import { error } from '@sveltejs/kit';
import games from '$lib/bookmaker/kiseki-books-full.json';

export function load({ params }) {
    for (const game of games) {
        const series = game.series.find((serie) => serie.slug === params.series);

        if (series) {
            return { series };
        }
    }
    
    throw error(404);
}