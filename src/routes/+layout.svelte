<script>
    import Sidebar from '$lib/svelte/Sidebar.svelte';
    import LanguagePicker from "$lib/svelte/LanguagePicker.svelte";
</script>

<main>
    <div class="header">
        <h1>kiseki-books</h1>
        <LanguagePicker />
    </div>

    <div class="content">
        <Sidebar />
        <!-- Viewer slot -->
        <slot />
    </div>
</main>

<style>
    @import '$lib/resources/global.css';

    main {
        margin: 0 20vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .header {
        margin-top: 1em;
        border-bottom: 1px #333 solid;
        display: flex;
        flex-direction: row;
        align-items: end;
        justify-content: space-between;
    }

    h1 {
        font-size: 3em;
        margin: 0;
    }

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

    @media (max-width: 1440px) {
        main {
            margin: 0 10vw;
        }
    }

    @media (max-width: 1080px) {
		main {
			max-width: none;
            margin: 0;
            padding: 8px 16px;
		}

        .header {
            flex-direction: column;
            align-items: start;
            margin: 0;
            padding-bottom: 8px;
        }

        h1 {
            font-size: 2em;
        }

        .content {
            flex-direction: column;
            overflow: visible;
            padding: 0;
        }
	}
</style>