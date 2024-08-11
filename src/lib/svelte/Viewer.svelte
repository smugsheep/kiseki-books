<script>
    import { lang } from '$lib/stores';
    import { page } from '$app/stores';
    import { base } from "$app/paths";
    import { goto } from '$app/navigation';
    import { browser } from '$app/environment';
    import { onMount } from 'svelte';

    export let selectedSeries;
    export let currentPart = 1;

    let currentTitle;
    let currentText;
    let viewer;
    let top;
    let prevSeriesID;

    $: currentPart, resetScroll();

    $: updateTitleAndText(selectedSeries, currentPart, $lang);

    function updateTitleAndText(series, part, lang) {
        if (prevSeriesID && series.id !== prevSeriesID) {
            currentPart = 1;
            part = 1;
        }

        prevSeriesID = series.id;

        if (browser && $page.url.pathname.includes(series.slug)) {
            setTimeout(() => {
                goto(`${base}/${series.slug}/${currentPart}`, false);
            }, 1);
        }

        let book = series.books.find(book => book.part == part);

        if (lang === 'en') {
            currentTitle = series.title;
            currentText = book.text_en;
            return;
        }
        
        currentTitle = series.title_ja;
        currentText = book.text_ja;
    }

    function changePart(direction) {
        if (direction === 'right' && currentPart < selectedSeries.books.length) {
            currentPart++;
        } else if (direction === 'left' && currentPart > 1) {
            currentPart--;
        }
    }

    async function resetScroll() {
        if (viewer && selectedSeries.id != 9999) {
            viewer.scrollTop = 0;
            top.parentElement.parentElement.scrollIntoView({ 
                behavior: 'auto', 
                block: 'start' 
            });
        }
    }

    function handleKeydown(event) {
        switch (event.key) {
            case 'ArrowRight':
                changePart('right');
                break;
            case 'ArrowLeft':
                changePart('left');
                break;
        }
    }

    onMount(() => {
        resetScroll();
        window.addEventListener('keydown', handleKeydown);

        return () => {
            window.removeEventListener('keydown', handleKeydown);
        };
    });
</script>

<div class="viewer-wrapper" bind:this={top}>
    <div class="top">
        <div>
            <h1>{currentTitle}</h1>
        </div>
        <div class="part-picker">
            <button 
                on:click={() => changePart('left')} 
                disabled={currentPart <= 1}
            >
                &larr;         
            </button>
    
            <select 
                bind:value={currentPart}
                disabled={selectedSeries.books.length < 2}
            >
                {#each selectedSeries.books as book}
                    <option value="{book.part}">
                        {
                            selectedSeries.books.length > 1 
                            ? ($lang === 'en' ? book.title : book.title_ja) 
                            : '-'
                        }
                    </option>
                {/each}
            </select>
    
            <button 
                on:click={() => changePart('right')} 
                disabled={currentPart >= selectedSeries.books.length}
            >
                &rarr;
            </button>
        </div>
    </div>
      
    <div id="viewer" bind:this={viewer}>
        <div>{@html currentText}</div>
    </div>
</div>

<style>
    @import '$lib/resources/scrollbar.css';

    .viewer-wrapper {
        display: flex;
        flex-direction: column;
        flex: 1;
        color: inherit;
    }

    .top {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: end;
        margin-bottom: .5em;
    }

    h1 {
        margin: 0;
    }

    .part-picker {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 0.5em;
    }

    select, option, button {
        height: 42px;
        background-color: var(--bg-white);
        font-family: inherit;
        font-size: var(--fs-norm);
        border: 1px solid var(--bg-gray);
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }

    button {
        background-color: var(--click-blue);
        color: white;
        border: none;
        padding: 0 1em;
    }

    button:disabled {
        background-color: var(--click-disabled);
        cursor: default;
    }

    button:hover:not(:disabled) {
        background-color: var(--click-blue-hover);
    }

    select {
        padding: 0 1em;
        max-width: 65vw;
    }

    select:focus {
        outline: none;
        border-color: var(--click-blue);
        box-shadow: 0 0 2px var(--click-blue-hover);
    }

    select:disabled {
        cursor: default;
    }

    #viewer {
        padding-right: 2em;
        font-size: var(--fs-reg);
        text-align: justify;
        height: 100%;
        overflow-y: scroll;
    }

    @media (max-width: 1080px) {
        #viewer, .part-picker {
            margin: 0;
            padding: 0;
        }

        #viewer {
            font-size: var(--fs-reg);
            padding-bottom: 5em;
        }

		.top {
            width: calc(100% - 32px);
            background: #313131;
            text-align: center;
            flex-direction: column;
            align-items: center;
            gap: .5em;
            position: fixed;
            bottom: 0;
            left: -16px;
            margin: 0;
            padding: .8em 2em;
        }
        
        h1 {
            font-size: var(--fs-big);
            color: white;
        }

        select, option, button {
            height: 32px;
            border-radius: 24px;
        }
	}

    @media (max-width: 768px) {
        #viewer, h1 {
            font-size: var(--fs-norm);
        }
    }
</style>