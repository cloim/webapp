<script>
    import { DarkMode } from 'flowbite-svelte';
</script>

<slot />
<div class="absolute bottom-0 left-0 w-[56px] p-2">
    <DarkMode class="text-primary-950 dark:text-primary-400 hover:bg-primary-200 dark:hover:bg-primary-700" />
</div>
