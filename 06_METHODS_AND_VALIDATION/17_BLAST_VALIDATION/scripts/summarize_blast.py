from pathlib import Path
import gzip, pandas as pd
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
ref=pd.read_csv(root/'reference/contig_to_organism.tsv',sep='\t').set_index('contig_id')['organism'].to_dict()
rows=[]
for f in sorted((root/'hits').glob('*.blast6.gz')):
    parts=f.name.replace('.blast6.gz','').split('__sub315147__rep')
    sample=parts[0].replace('EMOBON_RFORMOSA_','S_').replace('_MERGED','')
    sample='S_'+sample[2:4]+'_'+sample[4:6]+'_'+sample[6:8]
    counts={}
    with gzip.open(f,'rt') as h:
        for line in h:
            s=line.split('\t')[1]; counts[ref.get(s,s)]=counts.get(ref.get(s,s),0)+1
    for org,n in counts.items(): rows.append((sample,parts[1],org,n,n/315147*1e6))
d=pd.DataFrame(rows,columns=['sample','replicate','target','hits','rpm'])
(root/'tables').mkdir(exist_ok=True); (root/'figures').mkdir(exist_ok=True)
d.to_csv(root/'tables/blast_replicate_counts.tsv',sep='\t',index=False)
m=d.groupby(['sample','target'],as_index=False).agg(mean_hits=('hits','mean'),mean_rpm=('rpm','mean'))
m.to_csv(root/'tables/blast_sample_mean.tsv',sep='\t',index=False)
p=m.pivot(index='sample',columns='target',values='mean_rpm').fillna(0); top=p.sum().nlargest(10).index; q=p[top]; q=q.div(q.sum(axis=1),axis=0)*100
ax=q.plot.bar(stacked=True,figsize=(12,6),width=.82,color=plt.cm.tab10.colors,edgecolor='white',linewidth=.3)
ax.set_title('BLAST validation — top 10 reference targets'); ax.set_ylabel('Relative abundance within top 10 BLAST targets (%)'); ax.set_ylim(0,100); ax.legend(bbox_to_anchor=(1.02,1),loc='upper left',frameon=False); plt.xticks(rotation=60,ha='right'); plt.tight_layout(); plt.savefig(root/'figures/BLAST_top10_targets_stacked_barplot.png',dpi=300)
