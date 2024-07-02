<script lang="ts">
    import { Badge } from 'flowbite-svelte';
    import { twMerge } from 'tailwind-merge';
    import type { FormSizeType, SelectOptionType } from 'flowbite-svelte';

    export let disabled: boolean = false;
    export let items: SelectOptionType<any>[] = [];
    export let value: (string | number)[] = [];
    export let size: FormSizeType = 'md';

    export let selectStyle: string = '';
    export let dropdownStyle: string = '';
    export let listItemStyle: string = '';
    export let listSelectedItemStyle: string = '';
    export let selectedItemStyle: string = '';
    export let placeholder: string = '';

    let selectElem: HTMLSelectElement;
    let selectItems: SelectOptionType<any>[] = items.filter((x) => value.includes(x.value));
    let show: boolean = false;

    const sizes = {
        sm: 'px-2 py-1 min-h-[2.4rem]',
        md: 'px-3 py-1 min-h-[2.7rem]',
        lg: 'px-4 py-2 min-h-[3.2rem]'
    };

    let selectClass: string;
    $: {
        const selectClassBase: string = 'relative flex justify-between gap-4 text-xs border rounded border-neutral-300';

        if (disabled) {
            selectClass = twMerge(
                selectClassBase,
                'cursor-not-allowed bg-neutral-300 text-neutral-400 hover:bg-neutral-300',
                selectStyle
            );
        } else {
            selectClass = twMerge(
                selectClassBase,
                'cursor-pointer hover:border-orange-300 dark:!bg-neutral-700 dark:!border-neutral-500 dark:hover:!border-orange-300',
                selectStyle
            );
        }
    }

    let dropdownClass: string;
    $: dropdownClass = twMerge(
        'absolute start-0 top-[calc(100%+5px)] flex flex-col gap-1 z-50 p-1 w-full max-h-64 overflow-y-scroll text-xs font-medium cursor-pointer border rounded',
        'border-neutral-300 bg-white dark:!border-neutral-500 dark:bg-neutral-700',
        dropdownStyle
    );

    let listItemClass: string;
    $: listItemClass = twMerge('p-2 text-nowrap hover:text-black hover:bg-orange-300', listItemStyle);

    let listSelectedItemClass: string;
    $: listSelectedItemClass = twMerge('bg-orange-300 text-black hover:text-white', listSelectedItemStyle);

    let selectedItemClass: string;
    $: selectedItemClass = twMerge('bg-neutral-200 text-neutral-600', selectedItemStyle);

    const selectOption = (select: SelectOptionType<any>) => {
        if (value.includes(select.value)) {
            clearThisOption(select);
        } else {
            if (!value.includes(select.value)) value = [...value, select.value];
        }
        selectElem.dispatchEvent(create_custom_event('input', select));
    };

    const clearAll = (e: MouseEvent) => {
        e.stopPropagation();
        value = [];
    };

    const clearThisOption = (select: SelectOptionType<any>) => {
        if (value.includes(select.value)) {
            value = value.filter((o) => o !== select.value);
        }
    };

    function create_custom_event(type: string, detail: any, { bubbles = false, cancelable = false } = {}) {
        return new CustomEvent(type, { detail, bubbles, cancelable });
    }

    function init(node: HTMLSelectElement, value: any) {
        const inital = value; // hack for below
        return {
            update: (value: any) => {
                selectItems = items.filter((x) => value.includes(x.value));
                // avoid initial event emitting
                if (value !== inital) {
                    // node.dispatchEvent(create_custom_event('input', selectItems));
                    node.dispatchEvent(create_custom_event('change', selectItems));
                }
            }
        };
    }
</script>

<select use:init="{value}" {...$$restProps} value="{value}" hidden multiple bind:this="{selectElem}" on:change on:input>
    {#each items as { value, name }}
        <option value="{value}">{name}</option>
    {/each}
</select>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div
    on:click="{() => !disabled && (show = !show)}"
    on:focusout="{() => (show = false)}"
    tabindex="-1"
    role="listbox"
    class="{twMerge(selectClass, sizes[size], $$props.class)}">
    <span class="flex flex-wrap items-center gap-2">
        {#if selectItems.length}
            {#each selectItems as item (item.name)}
                <slot item="{item}" clear="{() => clearThisOption(item)}">
                    <Badge
                        class="{selectedItemClass}"
                        large="{size === 'lg'}"
                        dismissable="{!disabled}"
                        params="{{ duration: 100 }}"
                        on:close="{() => clearThisOption(item)}">
                        {item.name}
                    </Badge>
                </slot>
            {/each}
        {:else}
            <span class="ml-1">
                {placeholder}
            </span>
        {/if}
    </span>
    <div class="ms-auto flex items-center gap-2">
        <svg class="ms-1 h-3 w-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{show ? 'm1 5 4-4 4 4' : 'm9 1-4 4-4-4'}"></path>
        </svg>
    </div>
    {#if show}
        <div on:click|stopPropagation role="presentation" class="{dropdownClass}">
            {#each items as item (item.name)}
                <div
                    on:click="{() => selectOption(item)}"
                    role="presentation"
                    class="{twMerge(listItemClass, selectItems.includes(item) && listSelectedItemClass)}">
                    {item.name}
                </div>
            {/each}
        </div>
    {/if}
</div>
