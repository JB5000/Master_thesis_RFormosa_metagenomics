from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
d=pd.read_csv(root/'tables/blast_replicate_counts.tsv',sep='\t')
d=d[d.target.eq('Perkinsus olseni')]
s=d.groupby('sample',as_index=False).agg(mean_hits=('hits','mean'),sd_hits=('hits','std'),mean_rpm=('rpm','mean'),sd_rpm=('rpm','std')).sort_values('sample')
fig,ax=plt.subplots(figsize=(11,5)); x=range(len(s))
ax.errorbar(x,s.mean_hits,yerr=s.sd_hits,fmt='-o',color='#33547a',ecolor='#33547a',lw=1.6,elinewidth=1,capsize=3,ms=4.5,mfc='white',mew=1.1)
ax.set_xticks(list(x)); ax.set_xticklabels(s['sample'],rotation=90,fontsize=8); ax.set_ylabel('Perkinsus olseni BLAST hits'); ax.set_xlabel('Sample date (S_YY_MM_DD)'); ax.set_ylim(0,(s.mean_hits+s.sd_hits).max()*1.12)
for sp in ('top','right'): ax.spines[sp].set_visible(False)
ax.yaxis.grid(True,color='#e6e6e6',lw=.7); ax.set_axisbelow(True); ax.margins(x=.02); fig.tight_layout()
root.joinpath('figures').mkdir(exist_ok=True); s.to_csv(root/'tables/Perkinsus_olseni_BLAST_hits_timeseries.tsv',sep='\t',index=False); fig.savefig(root/'figures/Perkinsus_olseni_BLAST_hits_timeseries.png',dpi=300)
