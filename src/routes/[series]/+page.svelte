<script>
    import Viewer from '$lib/svelte/Viewer.svelte';

    export let data;
</script>

<Viewer selectedSeries={data.series}/>