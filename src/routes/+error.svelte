<script>
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';

    const redirect = () => {
        console.log($page.error);
        // goto(data.url);
    };
</script>

<div class="flex h-full w-full flex-col items-center justify-center gap-2">
    <span class="text-8xl font-extrabold">error</span>
    <span class="">{$page.error.message}</span>
    <button class="btn rounded mt-6" on:click="{redirect}">확인</button>
</div>
