<script>
    import { PUBLIC_APP_NAME } from '$env/static/public';
    import '../app.pcss';
</script>

<svelte:head>
  <title>{PUBLIC_APP_NAME}</title>
</svelte:head>

<slot />
