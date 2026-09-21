from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
root=Path('.')
g=pd.read_csv(root/'eqdepth_mean23_genus_relative_abundance_matrix.tsv',sep='\t',index_col=0)
g=g[[c for c in g if c.strip().lower() not in {'homo','synthetic construct'}]]
top=g.mean().nlargest(10).index
d=g[top].copy()
d=d.div(d.sum(axis=1),axis=0)*100
ax=d.plot.bar(stacked=True,figsize=(7.1,6.8),width=.82,color=list(plt.cm.tab10.colors),edgecolor='white',linewidth=.3)
ax.set_title('B  Top 10 genus stacked barplot',fontsize=10.5,fontweight='bold',loc='left')
ax.set_ylabel('Relative abundance within the top 10 genera (%)')
ax.set_xlabel('Sample date (S_YY_MM_DD)'); ax.set_ylim(0,100); ax.margins(x=.01)
ax.legend(ncol=2,fontsize=7.2,loc='lower left',frameon=True,facecolor='white',edgecolor='#cccccc',framealpha=.96)
ax.tick_params(axis='x',labelrotation=90,labelsize=7.5)
for sp in ('top','right'): ax.spines[sp].set_visible(False)
plt.tight_layout()
Path('figures_preview').mkdir(exist_ok=True)
plt.savefig('figures_preview/Fig_3.3B_top10_genus_barplot_top10_only.png',dpi=300)
