<script>
    import data from '$lib/bookmaker/kiseki-books-full.json';
    import { Hamburger, Close } from '$lib/resources/icons';
    import { lang } from '$lib/stores';
    import { page } from '$app/stores';
    
    let sidebar;
    let sidebarOpen = false;
    let sectionsClosed = {};

    function getTitle(obj, lang) {
        if (lang === 'en') {
            return obj.title;
        } else {
            return obj.title_ja;
        }
    }

    function toggleSection(id) {
        sectionsClosed[id] = !sectionsClosed[id];
    }

    function toggleSidebar() {
        sidebarOpen = !sidebarOpen;
    }

    const handleSeriesClick = () => {
        sidebarOpen = false;
    };

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
    {@html (sidebarOpen ? Hamburger : Close)}
</button>

<div class="sidebar {sidebarOpen ? 'open' : ''}" bind:this={sidebar}>
    <ul>
    {#each data as game}
        <div class='section'>
            
            <!-- game divider -->
            
            <button 
                class="game-divider"
                on:click={() => toggleSection(game.id)}
            >
                <span>{sectionsClosed[game.id] ? '＋' : '－'}</span>
                {getTitle(game, $lang)}
            </button>

            <!-- books for game -->
    
            {#if !sectionsClosed[game.id]}
            {#each game.series as series}
                <li class="book-item">
                    <a
                        href="/{series.slug}?part=1"
                        class="{
                            (series.slug === $page.params.series) 
                            ? 'selected' 
                            : ''
                        }"
                        on:click={() => handleSeriesClick(series)}
                    >
                        {getTitle(series, $lang)}
                    </a>
                </li>
            {/each}
            {/if}

        </div>
    {/each}
    </ul>
</div>

<style>
    @import '$lib/resources/scrollbar.css';

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

    button, a {
        font-size: 1.28em;
        background: none;
        border: none;
        padding: 0;
        color: rgb(26, 135, 189);
        cursor: pointer;
        text-align: left;
        display: block;
        max-width: 100%;
        white-space: nowrap; 
        overflow: hidden;
        text-overflow: ellipsis;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    a.selected {
        font-weight: 700;
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
