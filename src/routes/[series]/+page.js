import data from '$lib/bookmaker/kiseki-books-full.json';

export function entries() {
    let entries = [];

    for (const game of data) {
        for (const series of game.series) {
            entries.push({ series: series.slug });
        }
    }

    return entries;
}