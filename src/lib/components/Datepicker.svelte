<script>
    import Icon from '@iconify/svelte';

    export let range = false;
    export let datepickerFormat = 'yyyy-mm-dd';
    export let datepickerOrientation = 'bottom';
    export let attribute = '';
    export let inputClass = 'text-sm !pl-8 w-[120px] cursor-pointer';

    $: setAttribute = (node, params) => {
        if (params) {
            node.setAttribute(params, '');
        }
    };
</script>

<svelte:head>
    <script src="/node_modules/flowbite/dist/datepicker.js" rel="external"></script>
</svelte:head>

{#if range}
    <div date-rangepicker class="flex items-center" datepicker-format="{datepickerFormat}" datepicker-orientation="{datepickerOrientation}">
        <div class="relative">
            <div class="pointer-events-none absolute inset-y-4 left-0 flex items-center pl-2">
                <Icon icon="mdi:calendar-month" class="h-[18px] w-[18px]" />
            </div>
            <input name="start" type="text" class="{inputClass}" placeholder="시작일 선택" />
        </div>
        <span class="mx-2">~</span>
        <div class="relative">
            <div class="pointer-events-none absolute inset-y-4 left-0 flex items-center pl-2">
                <Icon icon="mdi:calendar-month" class="h-[18px] w-[18px]" />
            </div>
            <input name="end" type="text" class="{inputClass}" placeholder="종료일 선택" />
        </div>
    </div>
{:else}
    <div class="relative">
        <div class="pointer-events-none absolute inset-y-4 left-0 flex items-center pl-2">
            <Icon icon="mdi:calendar-month" class="h-[18px] w-[18px]" />
        </div>
        <input
            {...$$restProps}
            datepicker
            datepicker-format="{datepickerFormat}"
            datepicker-orientation="{datepickerOrientation}"
            datepicker-title=""
            use:setAttribute="{attribute}"
            type="text"
            class="{inputClass}"
            placeholder="날짜 선택" />
        <slot />
    </div>
{/if}
