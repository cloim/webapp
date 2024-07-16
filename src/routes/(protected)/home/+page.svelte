<script>
    import Select from '$components/Select.svelte';
    import MultiSelect from '$components/MultiSelect.svelte';
    import Dialog from '$components/Dialog.svelte';

    const items = [
        { value: 'warn', name: 'warn' },
        { value: 'err', name: 'err' },
        { value: 'confirm', name: 'confirm' },
        { value: 'input', name: 'input' },
        { value: 'loading', name: 'loading' },
    ]

    let dialog;
    let selectValue = 'warn';
    let multiSelectValue = ['err', 'input'];

    const handleClick = () => {
        dialog.show(selectValue, `This is a ${selectValue} dialog.`, {
            onDialogButtonClicked: (btnID) => {
                console.log(btnID);
            }
        });
    }
</script>

<div class="h-full w-full p-2 flex flex-col gap-2">
    <div class="flex flex-row gap-2">
        <Select class="flex-1" {items} bind:value={selectValue} />
        <button class="btn rounded" on:click={handleClick}>Show</button>
    </div>
    <div>
        <MultiSelect {items} bind:value={multiSelectValue} />
    </div>
</div>
<Dialog bind:this="{dialog}" />