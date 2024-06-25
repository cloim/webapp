<script>
    import { Modal } from 'flowbite-svelte';
    import Icon from '@iconify/svelte';

    let open = false;
    let buttonPrimary = 'bg-[#0e639c] hover:bg-[#1177bb] active:bg-[#1177bb] focus:!border-none';
    let buttonSecondary = 'bg-[#4d4d4d] hover:bg-[#636363] active:bg-[#3c3c3c] focus:!border-none';

    let type;
    let title;
    let iconID;
    let iconColor;
    let message;
    let dismissable;
    let handler;

    export const show = (_type, _message, _handler) => {
        type = _type;

        switch (type) {
            case 'warn':
                title = '';
                iconID = 'mdi:alert-octagon-outline';
                iconColor = 'yellow';
                dismissable = true;
                break;

            case 'err':
                title = '';
                iconID = 'mdi:alert-octagon-outline';
                iconColor = 'red';
                dismissable = true;
                break;

            case 'confirm':
                title = '';
                iconID = 'line-md:circle-to-confirm-circle-transition';
                iconColor = '#1177bb';
                dismissable = true;
                break;

            case 'input':
                title = '';
                iconID = 'mdi:help-circle-outline';
                iconColor = '#1177bb';
                dismissable = true;
                break;

            case 'loading':
                title = '';
                iconID = 'line-md:loading-loop';
                iconColor = '#1177bb';
                dismissable = false;
                break;

            default:
                title = '';
                iconID = 'mdi:information-outline';
                iconColor = '';
                dismissable = true;
                break;
        }
        message = _message;
        handler = _handler;
        open = true;
    };

    export const dismiss = () => {
        open = false;
    };
</script>

<Modal title="{title}" bind:open="{open}" size="xs" autoclose dismissable="{dismissable}" class="divide-y-0 rounded-none bg-[#424242] text-[#cccccc]">
    <div class="flex flex-col gap-8">
        <div class="flex flex-row gap-4 pr-5">
            <Icon icon="{iconID}" color="{iconColor}" class="h-12 w-12" />
            <p class="flex-1 self-center">
                {@html message}
            </p>
        </div>
        {#if type === 'input'}
            <div>
                <input type="text" class="w-full text-xs text-black" />
            </div>
        {/if}
        {#if type !== 'loading'}
            <div class="flex justify-end gap-2">
                <button type="button" class="{buttonPrimary}" on:click="{(e) => handler?.onDialogButtonClicked('ok')}"> 확인 </button>
                {#if ['confirm', 'input'].indexOf(type) > -1}
                    <button type="button" class="{buttonSecondary}" on:click="{(e) => handler?.onDialogButtonClicked('cancel')}"> 취소 </button>
                {/if}
            </div>
        {/if}
    </div>
</Modal>

<style lang="postcss">
    button {
        @apply items-center justify-center px-5 py-2.5 text-center text-sm font-medium;
    }
</style>
