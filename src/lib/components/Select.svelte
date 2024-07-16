<script lang="ts">
    import { twMerge } from 'tailwind-merge';
    import type { FormSizeType, SelectOptionType } from 'flowbite-svelte';

    export let disabled: boolean = false;
    export let items: SelectOptionType<any>[] = [];
    export let value: string | number = '';
    export let size: FormSizeType = 'md';

    export let selectStyle: string = '';
    export let dropdownStyle: string = '';
    export let listItemStyle: string = '';
    export let listSelectedItemStyle: string = '';
    export let placeholder: string = '';

    const sizes = {
        sm: 'px-2 py-1 min-h-[2.4rem]',
        md: 'px-3 py-1 min-h-[2.7rem]',
        lg: 'px-4 py-2 min-h-[3.2rem]'
    };

    let show: boolean = false;
    let selectElem: HTMLSelectElement;
    let selectItem: SelectOptionType<any>;
    $: {
        selectItem = items.filter((x) => value == x.value)[0];
    }

    let selectClass: string;
    $: {
        const selectClassBase: string = 'relative flex justify-between gap-4 text-sm border rounded';

        if (disabled) {
            selectClass = twMerge(
                selectClassBase,
                'cursor-not-allowed',
                'bg-primary-300 text-primary-400 border-primary-400',
                selectStyle
            );
        } else {
            selectClass = twMerge(
                selectClassBase,
                'cursor-pointer',
                'bg-white border-primary-400',
                'dark:bg-primary-800 dark:border-primary-600',
                'hover:border-accent-100',
                selectStyle
            );
        }
    }

    let dropdownClass: string;
    $: dropdownClass = twMerge(
        'absolute start-0 top-[calc(100%+5px)] flex flex-col gap-1 z-50 p-1 w-full max-h-64 overflow-y-scroll text-sm font-medium cursor-pointer border rounded',
        'bg-white dark:bg-primary-800 border-primary-400 dark:border-primary-600',
        dropdownStyle
    );

    let listItemClass: string;
    $: listItemClass = twMerge('p-2 text-nowrap hover:text-white hover:bg-accent-100', listItemStyle);

    let listSelectedItemClass: string;
    $: listSelectedItemClass = twMerge('bg-accent-200 text-primary-200 hover:text-white', listSelectedItemStyle);

    const selectOption = (select: SelectOptionType<any>) => {
        value = select.value;
        selectElem.dispatchEvent(create_custom_event('input', select));
        show = true;
    };

    function create_custom_event(type: string, detail: any, { bubbles = false, cancelable = false } = {}) {
        return new CustomEvent(type, { detail, bubbles, cancelable });
    }

    function init(node: HTMLSelectElement, value: any) {
        const inital = value; // hack for below
        return {
            update: (value: any) => {
                if (value) {
                    selectItem = items.filter((x) => value == x.value)[0];
                    // avoid initial event emitting
                    if (value !== inital) {
                        // node.dispatchEvent(create_custom_event('input', selectItem));
                        node.dispatchEvent(create_custom_event('change', selectItem));
                    }
                } else {
                    selectItem = null;
                }
            }
        };
    }
</script>

<select use:init="{value}" {...$$restProps} value="{value}" hidden bind:this="{selectElem}" on:change on:input>
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
    <span class="ml-1 flex flex-wrap gap-2 self-center">
        {#if selectItem}
            {selectItem.name}
        {:else}
            <span class="text-primary-500">
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
        <div class="{dropdownClass}">
            {#each items as item (item.name)}
                <div on:click="{() => selectOption(item)}" role="presentation" class="{twMerge(listItemClass, item.value == value && listSelectedItemClass)}">
                    {item.name}
                </div>
            {/each}
        </div>
    {/if}
</div>
