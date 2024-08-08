<script>
    import LanguagePicker from "../lib/svelte/LanguagePicker.svelte";
</script>

<main>
    <div class="header">
        <h1>kiseki-books</h1>
        <LanguagePicker />
    </div>

    <slot />

</main>

<style>
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

    @media (max-width: 1280px) {
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
	}
</style>