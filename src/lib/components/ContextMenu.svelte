<script lang="ts" context="module">
    export interface Position {
        x: number;
        y: number;
    }

    export interface ContextMenuItem {
        group: string;
        id: string;
        title: string;
    }
</script>

<script lang="ts">
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    let _show: boolean = false;
    let _pos: Position = {x: 0, y: 0};
    let _menuItems: ContextMenuItem[] = [];
    let _filteredItems: ContextMenuItem[] = [];
    let _targetItem: unknown = null;

    export function registerMenu(menuItems: ContextMenuItem[]) {
        _menuItems = menuItems;
        _filteredItems = menuItems;
    }

    export function showMenu(show: boolean, group?: string, pos?: Position, targetItem?: unknown) {
        if (group) _filteredItems = _menuItems.filter((item) => item.group == group);
        if (pos) _pos = pos;
        if (targetItem) _targetItem = targetItem;
        _show = show;
    }
</script>

{#if _show}
    <div class="contextmenu" style="top: {_pos.y}px; left: {_pos.x}px;">
        {#each _filteredItems as menuItem}
            <div class="menuitem" role="presentation" on:click={(e) => {
                    dispatch("itemClicked", { itemID: menuItem.id, target: _targetItem });
                }}
            >
                {menuItem.title}
            </div>
        {/each}
    </div>
{/if}

<svelte:window on:click={(e) => _show = false} />

<style lang="postcss">
    .contextmenu {
        @apply absolute flex flex-col gap-1 rounded-md overflow-hidden border z-50;
        @apply bg-primary-200 border-primary-300;
        @apply dark:bg-primary-800 dark:border-primary-600;
    }

	.contextmenu .menuitem {
        @apply px-3 py-1 min-w-[100px] cursor-pointer text-sm overflow-hidden;
        @apply hover:bg-primary-100 active:bg-primary-200;
        @apply dark:hover:bg-primary-700;
	}
</style>