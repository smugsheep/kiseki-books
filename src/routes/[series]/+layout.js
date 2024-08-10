import { error } from '@sveltejs/kit';
import games from '$lib/bookmaker/kiseki-books-full.json';

export function load({ params }) {
    for (const game of games) {
        const series = game.series.find((serie) => serie.slug === params.series);

        if (series) {
            if (params.part > series.books.length) {
                params.part = 1;
            }

            return { 
                series: series, 
                part: params.part 
            };
        }
    }
    
    throw error(404);
}