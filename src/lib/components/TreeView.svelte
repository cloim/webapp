<script>
    import { createEventDispatcher } from 'svelte';
    import { writable } from "svelte/store";
    import Icon from "@iconify/svelte";
    import TreeViewTree from "./TreeViewTree.svelte";

    export let items;
    
    const dispatch = createEventDispatcher();
    const expandStates = writable([]);
    
    let expanded = false;
    let searchKey = "";
    let treeItems = [];

    $: {
        treeItems = items;
    }

    const onSearch = () => {
        function search(obj) {
            let filtered = [];

            if (obj.children) {
                for (const c of obj.children) {
                    if (c.children) {
                        const temp = search(c);
                        if (temp) filtered.push(temp);
                    } else if (c.name.indexOf(searchKey) > -1 || c.desc.indexOf(searchKey) > -1) {
                        filtered.push(c);
                    }
                }
            }

            if (filtered.length > 0) {
                return {
                    ...obj,
                    children: filtered
                };
            } else {
                return null;
            }
        }

        const s = search({children: items});
        if (s) {
            treeItems = s.children;
        } else {
            treeItems = [];
        }
    }

    const reloadData = () => {
        dispatch("reloadData");
    }

    const expandAll = (nodes, expand) => {
        for (const node of nodes) {
            if (node.children) {
                $expandStates[node.id] = expand;
                expandAll(node.children, expand);
            }
        }
        expanded = expand;
    }
</script>

<div class="h-full flex flex-col overflow-x-hidden">
    <div class="sticky top-0 z-10 pb-2 bg-primary-150 dark:bg-primary-900">
        <div class="text-xs p-2">
            탐색기
        </div>
        <div class="flex px-2 gap-1">
            <input type="text" class="input flex-1" bind:value={searchKey} on:change={onSearch} />
            <button class="px-2 rounded hover:bg-primary-300 dark:hover:bg-primary-700" on:click={reloadData}>
                <Icon icon="mdi:refresh" width="14" height="14" />
            </button>
            <button class="px-2 rounded hover:bg-primary-300 dark:hover:bg-primary-700" on:click={(e) => expandAll(items, !expanded)}>
                <Icon icon="{expanded ? 'mdi:arrow-collapse-all' : 'mdi:arrow-expand-all'}" width="14" height="14" />
            </button>
        </div>
    </div>
    <div class="flex-1">
        <TreeViewTree items={treeItems} {expandStates} on:doubleClicked on:contextMenuRequested />
    </div>
</div>