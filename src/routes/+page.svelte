<script>
    import Sidebar from '../lib/svelte/Sidebar.svelte';
    import Viewer from '../lib/svelte/Viewer.svelte';

    let currentSeries;

    const handleSeriesChange = (series) => {
        currentSeries = series;
    };
</script>

<div class="content">
    <Sidebar onSeriesClick={handleSeriesChange} />
    <Viewer selectedSeries={currentSeries} />
</div>

<style>
    .content {
        display: flex;
        flex-direction: row;
        flex-grow: 1;
        padding-top: 1em;
        overflow: hidden;
        margin-bottom: 1em;
        justify-content: space-between;
        gap: 2em;
    }

    @media (max-width: 1280px) {
        .content {
            flex-direction: column;
            overflow: visible;
        }
	}
</style>