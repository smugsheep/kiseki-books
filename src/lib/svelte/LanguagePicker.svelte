<script>
    import { base } from "$app/paths";
    import { lang } from '../stores.js';

    const toggleLang = () => {
        lang.set($lang === 'en' ? 'ja' : 'en');
    };
</script>

<nav>
    <a href="{base}/" class="nav-item">
        home
    </a>
    <!-- <a href="{base}/about" class="nav-item">
        about
    </a> -->
    <a href="" class="nav-item" on:click={toggleLang}>
        switch to {$lang === 'en' ? '日本語' : 'English'}
    </a>
</nav>

<style>
    nav {
        display: flex;
        flex-direction: row;
        padding: 0.3em 0;
    }

    .nav-item {
        font-size: 1.28em;
        background: none;
        border: none;
        text-decoration: none;
        cursor: pointer;
        display: flex;
        flex-direction: row;
        align-items: end;
        white-space: nowrap;
    }

    .nav-item:hover {
        color: #007bff;
    }

    .nav-item:not(:last-child)::after {
        padding: 0 8px;
        content: '/';
        color: #333;
    }

    a, a:visited {
        color: inherit;
    }

    @media (max-width: 1080px) {
		nav, .nav-item {
            padding: 0;
        }
	}
</style>