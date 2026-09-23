from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data = pd.read_csv(root / 'tables/blast_replicate_counts.tsv', sep='\t')
    data = data[data.target.eq('Perkinsus olseni')]
    summary = data.groupby('sample', as_index=False).agg(
        mean_hits=('hits', 'mean'), sd_hits=('hits', 'std'),
        mean_rpm=('rpm', 'mean'), sd_rpm=('rpm', 'std'),
    ).sort_values('sample')
    fig, ax = plt.subplots(figsize=(11, 5))
    x = range(len(summary))
    ax.errorbar(
        x, summary.mean_hits, yerr=summary.sd_hits, fmt='-o',
        color='#33547a', ecolor='#33547a', lw=1.6, elinewidth=1,
        capsize=3, ms=4.5, mfc='white', mew=1.1,
    )
    ax.set_xticks(list(x))
    ax.set_xticklabels(summary['sample'], rotation=90, fontsize=8)
    ax.set_ylabel('Perkinsus olseni BLAST hits')
    ax.set_xlabel('Sample date (S_YY_MM_DD)')
    ax.set_ylim(0, (summary.mean_hits + summary.sd_hits).max() * 1.12)
    for spine in ('top', 'right'):
        ax.spines[spine].set_visible(False)
    ax.yaxis.grid(True, color='#e6e6e6', lw=.7)
    ax.set_axisbelow(True)
    ax.margins(x=.02)
    fig.tight_layout()
    (root / 'tables').mkdir(parents=True, exist_ok=True)
    (root / 'figures').mkdir(parents=True, exist_ok=True)
    summary.to_csv(root / 'tables/Perkinsus_olseni_BLAST_hits_timeseries.tsv', sep='\t', index=False)
    fig.savefig(root / 'figures/Perkinsus_olseni_BLAST_hits_timeseries.png', dpi=300)


if __name__ == '__main__':
    main()
