<script>
    import { lang } from '../stores';
    import { onMount, tick } from 'svelte';
    export let selectedSeries = { 
        title: 'Welcome.',
        title_ja: 'ようこそ。',
        id: 9999,
        books: [{ 
            part: 1, 
            text_en: '<blockquote>Choose a series from the menu to read.</blockquote>',
            text_ja: '<blockquote>メニュからシリーズを選んでください。</blockquote>',
        }] 
    };

    let currentPart = 1;
    let prevID = selectedSeries.id;

    // Reactive statement to reset currentPart and scroll to top when selectedSeries changes
    $: if (prevID !== selectedSeries.id) {
        currentPart = 1;
        prevID = selectedSeries.id;
        resetScroll();
    }

    // Reactive statement to handle currentPart change
    $: currentPart, resetScroll();

    let currentTitle;
    let currentText;

    $: updateTitleAndText(selectedSeries, currentPart, $lang);

    function updateTitleAndText(series, part, lang) {
        let book = series.books.find(book => book.part === part);

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

    let viewer;
    let top;

    async function resetScroll() {
        if (viewer && selectedSeries.id != 9999) {
            viewer.scrollTop = 0;
            top.parentElement.parentElement.scrollIntoView({ behavior: 'auto', block: 'start' });
        }
    }

    function handleKeydown(event) {
        if (event.key === 'ArrowRight') {
            changePart('right');
        } else if (event.key === 'ArrowLeft') {
            changePart('left');
        }
    }

    // Call resetScroll when component mounts
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
                    <option 
                        value="{book.part}">{selectedSeries.books.length > 1 ? ($lang === 'en' ? book.title : book.title_ja) : '-'}
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
    @import '../resources/scrollbar.css';

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

    .viewer-wrapper {
        display: flex;
        flex-direction: column;
        flex: 1;
    }

    .part-picker {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 0.5em; /* Add space between elements */
    }

    select, option, button {
        font-family: inherit;
        font-size: 100%;
        font-size: 1em;
        height: 42px;
        border: 1px solid #ccc;
        border-radius: 4px;
        background-color: #f9f9f9;
        cursor: pointer;
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }

    button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 0 1em;
    }

    button:disabled {
        background-color: #ddd;
        cursor: default;
    }

    button:hover:not(:disabled) {
        background-color: #0056b3;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    select {
        padding: 0 1em;
        max-width: 65vw;
    }

    select:focus {
        outline: none;
        border-color: #007bff;
        box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
    }

    select:disabled {
        cursor: default;
    }

    #viewer {
        padding-right: 2em;
        font-size: 1.5em;
        text-align: justify;
        height: 100%;
        overflow-y: scroll;
    }

    @media (max-width: 1280px) {
        #viewer, .part-picker {
            margin: 0;
            padding: 0;
        }

		.top {
            flex-direction: column;
            align-items: center;
            gap: .5em;
            /* position: sticky;
            top: 0; 
            padding-bottom: 0.5em; */
            background: #313131;
            text-align: center;

            width: calc(100% - 32px);
            bottom: 0;
            left: -16px;
            position: fixed;
            margin: 0;
            padding: 1em 2em;
        }
        
        h1 {
            font-size: 1.4em;
            color: white;
        }

        #viewer {
            font-size: 1.4em;
            padding-bottom: 6em;
        }

        select, option, button {
            height: 32px;
            border-radius: 24px;
        }
	}
</style>