<script>
    import Viewer from '$lib/svelte/Viewer.svelte';

    const welcome = { 
        title: 'Welcome.',
        title_ja: 'ようこそ。',
        id: 9999,
        books: [{ 
            part: 1, 
            text_en: '<blockquote>Choose a series from the menu to read.</blockquote>',
            text_ja: '<blockquote>メニュからシリーズを選んでください。</blockquote>',
        }] 
    };
</script>

<Viewer selectedSeries={welcome}/>