<script>
    import { lang } from '../stores.js';

    const toggleLang = () => {
        lang.set($lang === 'en' ? 'ja' : 'en');
    };
</script>

<div>
    <button on:click={toggleLang}>
        switch to
        {#if $lang === 'en'}
            <span>日本語</span>
        {:else if $lang === 'ja'}
            <span>English</span>
        {/if}
    </button>
</div>

<style>
    button {
        font-size: 1.28em;
        background: none;
        border: none;
        cursor: pointer;
        padding: 0.3em 0;
        display: flex;
        flex-direction: row;
        align-items: end;
        white-space: nowrap;
    }

    button:hover {
        color: #007bff;
    }
    
    span::before {
        content: '\00a0';
    }

    @media (max-width: 1280px) {
		button {
            padding: 0;
        }
	}
</style>