from pathlib import Path
import gzip, pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    ref = pd.read_csv(root / 'reference/contig_to_organism.tsv', sep='\t').set_index('contig_id')['organism'].to_dict()
    rows = []
    for f in sorted((root / 'hits').glob('*.blast6.gz')):
        parts = f.name.replace('.blast6.gz', '').split('__sub315147__rep')
        sample = parts[0].replace('EMOBON_RFORMOSA_', 'S_').replace('_MERGED', '')
        sample = 'S_' + sample[2:4] + '_' + sample[4:6] + '_' + sample[6:8]
        counts = {}
        with gzip.open(f, 'rt') as handle:
            for line in handle:
                subject = line.split('\t')[1]
                organism = ref.get(subject, subject)
                counts[organism] = counts.get(organism, 0) + 1
        for organism, count in counts.items():
            rows.append((sample, parts[1], organism, count, count / 315147 * 1e6))

    d = pd.DataFrame(rows, columns=['sample', 'replicate', 'target', 'hits', 'rpm'])
    (root / 'tables').mkdir(parents=True, exist_ok=True)
    (root / 'figures').mkdir(parents=True, exist_ok=True)
    d.to_csv(root / 'tables/blast_replicate_counts.tsv', sep='\t', index=False)
    means = d.groupby(['sample', 'target'], as_index=False).agg(
        mean_hits=('hits', 'mean'), mean_rpm=('rpm', 'mean')
    )
    means.to_csv(root / 'tables/blast_sample_mean.tsv', sep='\t', index=False)
    pivot = means.pivot(index='sample', columns='target', values='mean_rpm').fillna(0)
    top = pivot.sum().nlargest(10).index
    composition = pivot[top]
    composition = composition.div(composition.sum(axis=1), axis=0) * 100
    ax = composition.plot.bar(
        stacked=True, figsize=(12, 6), width=.82,
        color=plt.cm.tab10.colors, edgecolor='white', linewidth=.3,
    )
    ax.set_title('BLAST validation — top 10 reference targets')
    ax.set_ylabel('Relative abundance within top 10 BLAST targets (%)')
    ax.set_ylim(0, 100)
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False)
    plt.xticks(rotation=60, ha='right')
    plt.tight_layout()
    plt.savefig(root / 'figures/BLAST_top10_targets_stacked_barplot.png', dpi=300)


if __name__ == '__main__':
    main()
