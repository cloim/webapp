<script>
    import { createEventDispatcher } from 'svelte';
    import Icon from "@iconify/svelte";

    export let items;
    export let depth = 0;
    export let expandStates;

    const dispatch = createEventDispatcher();
</script>

<div>
    {#each items as item}
        <div class="flex pr-2 pb-[2px] text-base hover:text-white hover:bg-accent-100 cursor-pointer items-center"
            style="padding-left: {(depth * 20) + 8}px" role="presentation"
            on:click={(e) => {
                if ($expandStates.hasOwnProperty(item.id)) {
                    $expandStates[item.id] = !$expandStates[item.id];
                } else {
                    $expandStates[item.id] = true;
                }
            }}
            on:dblclick={(e) => { if (!item.children) dispatch("doubleClicked", item); }}
            on:contextmenu|preventDefault={(e) => dispatch("contextMenuRequested", 
                { from: "TreeViewTree", item, x: e.clientX, y: e.clientY }
            )}
        >
            {#if item.children}
                <div class="pt-[3px]" class:arrow-down={$expandStates[item.id]}>
                    <Icon icon="ic:baseline-chevron-right" class="pb-[1px] w-[18px] h-[20px]" />
                </div>
            {:else}
                <div class="pt-[3px] mr-2">
                    <Icon icon="{item.iconID}" color={item.iconColor} />
                </div>
            {/if}
            <div class="pb-[1px] mr-2">
                {item.name}
            </div>
            <div class="pt-[2px] whitespace-nowrap text-xs text-primary-400 dark:text-primary-500">
                {item.children ? "" : item.desc}
            </div>
        </div>
        {#if $expandStates[item.id] && item.children}
            <div>
                <svelte:self items={item.children} depth={depth + 1} {expandStates} on:doubleClicked on:contextMenuRequested />
            </div>
        {/if}
    {/each}
</div>

<style lang="postcss">
    .arrow-down {
        @apply rotate-90 pl-[4px] pt-[1px];
    }
</style>