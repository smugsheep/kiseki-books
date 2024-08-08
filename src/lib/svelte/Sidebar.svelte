<script>
    import data from '../bookmaker/kiseki-books-full.json';
    import { lang } from '../stores';

	export let onSeriesClick;

    let selected;

    const handleSeriesClick = (series) => {
        selected = series;
        onSeriesClick(series);
        sidebarOpen = false;
    };

    function getTitle(obj, lang) {
        if (lang === 'en') {
            return obj.title;
        } else {
            return obj.title_ja;
        }
    }

    let sectionsClosed = {};

    function toggleSection(id) {
        sectionsClosed[id] = !sectionsClosed[id];
    }

    let sidebar;
    let sidebarOpen = false;

    function toggleSidebar() {
        sidebarOpen = !sidebarOpen;
    }

    function handleOutsideClick(event) {
        if (sidebarOpen 
            && !event.target.closest('.sidebar') 
            && !event.target.closest('.sidebar-toggle')
            && !event.target.closest('svg')) {
            sidebarOpen = false;
        }
    }

    $: if (sidebarOpen) {
        sidebar.parentElement.addEventListener('click', handleOutsideClick);
    }

</script>

<button class="sidebar-toggle" on:click={toggleSidebar}>
    {#if sidebarOpen}
        <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg"><path d="m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z"></path></svg>
    {:else}
        <svg stroke="currentColor" fill="none" stroke-width="0" viewBox="0 0 15 15" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M1.5 3C1.22386 3 1 3.22386 1 3.5C1 3.77614 1.22386 4 1.5 4H13.5C13.7761 4 14 3.77614 14 3.5C14 3.22386 13.7761 3 13.5 3H1.5ZM1 7.5C1 7.22386 1.22386 7 1.5 7H13.5C13.7761 7 14 7.22386 14 7.5C14 7.77614 13.7761 8 13.5 8H1.5C1.22386 8 1 7.77614 1 7.5ZM1 11.5C1 11.2239 1.22386 11 1.5 11H13.5C13.7761 11 14 11.2239 14 11.5C14 11.7761 13.7761 12 13.5 12H1.5C1.22386 12 1 11.7761 1 11.5Z" fill="currentColor"></path></svg>
    {/if}
</button>

<div class="sidebar {sidebarOpen ? 'open' : ''}" bind:this={sidebar}>
    <ul>
        {#each data as game}
            <div class='section'>
                <button 
                    class="game-divider"
                    on:click={() => toggleSection(game.id)}
                >
                    <span>{sectionsClosed[game.id] ? '＋' : '－'}</span>
                    {getTitle(game, $lang)}
                </button>
        
                {#if !sectionsClosed[game.id]}
                    {#each game.series as series}
                        <li class="book-item">
                            <button 
                                class="{(series === selected) ? 'selected' : ''}"
                                on:click={() => handleSeriesClick(series)}
                            >
                                {getTitle(series, $lang)}
                            </button>
                        </li>
                    {/each}
                {/if}
            </div>
        {/each}
    </ul>
</div>

<style>
    @import '../resources/scrollbar.css';

    ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        padding-right: 1em;
        width: 240px;
        height: 100%;
        overflow-y: scroll;
    }

    .section {
        margin-bottom: .5em;
    }

    .game-divider {
        margin: 0;
        text-transform: uppercase;
        font-size: 1.2em;
        color: #313131;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .game-divider span {
        font-size: 0.8em;
    }

    .game-divider:hover {
        color: #5a5a5a;
    }

    button {
        font-size: 1.28em;
        background: none;
        border: none;
        padding: 0;
        color: rgb(26, 135, 189);
        cursor: pointer;
        text-align: left;
        max-width: 100%;
        white-space: nowrap; 
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .selected {
        font-weight: 700;
    }

    .book-item button:hover {
        text-decoration: underline;
    }

    .sidebar {
        transition: transform 0.25s ease;
    }

    @media (max-width: 1280px) {
        .sidebar {
            position: fixed;
            top: 0;
            right: 0;
            height: 100%;
            width: 80%;
            background-color: white;
            box-shadow: -4px 0 40px rgba(0, 0, 0, 0.4);
            transform: translateX(103%);
            z-index: 999;
        }

        .sidebar.open {
            transform: translateX(0);
        }

        .sidebar-toggle {
            position: fixed;
            width: 56px;
            height: 56px;
            padding: 16px;
            border-radius: 4px;
            top: 10px;
            right: 10px;
            background-color: #313131;
            color: white;
            border: none;
            cursor: pointer;
            z-index: 1000;
        }

        ul {
            width: 100%;
            height: 100%;
		}

        .section {
            padding: 0 2em;
        }

        .section:first-child {
            padding-top: 2em;
        }

        .section:last-child {
            padding-bottom: 2em;
        }
    }

    @media (min-width: 1280px) {
        .sidebar-toggle {
            display: none;
        }
    }
</style>
