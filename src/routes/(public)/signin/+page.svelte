<script>
    import { PUBLIC_APP_NAME } from '$env/static/public';
    import { goto } from '$app/navigation';
    import Dialog from '$components/Dialog.svelte';

    let dialog;
    let uid;
    let upw;

    const signup = async (e) => {
        goto('/signup');
    };

    const signin = async (e) => {
        const res = await fetch('/api/signin', {
            method: 'POST',
            body: JSON.stringify({ uid, upw })
        });
        const res_data = await res.json();

        if (res_data.status == 200) {
            goto('/');
        } else {
            dialog.show('err', res_data.message);
        }
    };
</script>

<div class="flex h-full justify-center">
    <div class="flex w-1/3 min-w-[350px] max-w-[390px] flex-col gap-10 self-center rounded-xl p-10">
        <div class="self-center font-bold">
            <h1>{PUBLIC_APP_NAME}</h1>
        </div>
        <div class="flex flex-col gap-2">
            <input class="input" type="text" bind:value="{uid}" placeholder="ID" />
            <input class="input" type="password" bind:value="{upw}" placeholder="Password" on:keydown="{(e) => e.key == 'Enter' && signin()}" />
            <button class="btn rounded" on:click="{signin}">Sign In</button>
            <button class="btn btn-border rounded" on:click="{signup}">Sign Up</button>
        </div>
    </div>
</div>
<Dialog bind:this="{dialog}" />
