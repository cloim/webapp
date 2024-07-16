<script>
    import { goto } from '$app/navigation';
    import Dialog from '$components/Dialog.svelte';

    let dialog;
    let uid;
    let uname;
    let upw;

    const signup = async (e) => {
        const res = await fetch('/api/signup', {
            method: 'POST',
            body: JSON.stringify({ uname, uid, upw })
        });
        const res_data = await res.json();

        if (res.status == 200) {
            goto('/');
        } else {
            dialog.show('err', res_data.detail);
        }
    };

    const back = async () => {
        goto('/signin');
    };
</script>

<div class="flex h-full justify-center">
    <div class="flex w-1/3 min-w-[350px] max-w-[390px] flex-col gap-4 self-center rounded-xl p-10">
        <div class="text-2xl font-bold">
            Sign Up
        </div>
        <div class="flex flex-col gap-2">
            <input class="input" type="text" bind:value="{uname}" placeholder="Name" />
            <input class="input" type="text" bind:value="{uid}" placeholder="ID" />
            <input class="input" type="password" bind:value="{upw}" placeholder="Password" />
            <button class="btn rounded" on:click="{signup}">Sign Up</button>
            <button class="btn-wire rounded" on:click="{back}">Back</button>
        </div>
    </div>
</div>
<Dialog bind:this="{dialog}" />
