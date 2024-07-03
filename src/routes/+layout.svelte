<script>
    import { onMount } from 'svelte';
    import { PUBLIC_APP_NAME } from '$env/static/public';
    import { theme } from '$lib/store';
    import '../app.pcss';

    onMount(() => {
        const html = document.getElementsByTagName('html')[0];
        const cur_theme = html.classList.contains('dark') ? 'dark' : 'light';
        theme.set(cur_theme);

        const observer = new MutationObserver((mutations) => {
            const new_theme = html.classList.contains('dark') ? 'dark' : 'light';
            theme.set(new_theme);
        });

        observer.observe(html, {
            attributes: true,
            attributeFilter: ['class'],
            childList: false,
            subtree: false
        });
    });
</script>

<svelte:head>
    <title>{PUBLIC_APP_NAME}</title>
</svelte:head>

<slot />
