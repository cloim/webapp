<script>
    import { PUBLIC_APP_NAME } from '$env/static/public';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { Tooltip, Dropdown, DropdownItem, DropdownDivider, DarkMode } from 'flowbite-svelte';
    import Icon from '@iconify/svelte';
    import { menuItems } from './MenuItems.svelte';
    import { theme } from '$lib/store';

    export let data;
    let sidebarElem;
    let isOpen = false;
    let activeUrl;

    $: {
        activeUrl = $page.url.pathname;
    }

    const toggleSidebar = () => {
        isOpen = !isOpen;

        if (isOpen) {
            sidebarElem.style.width = 'auto';
            sidebarElem.style.minWidth = '300px';
            sidebarElem.style.maxWidth = '300px';
        } else {
            sidebarElem.style.width = 'auto';
            sidebarElem.style.minWidth = '49px';
            sidebarElem.style.maxWidth = '49px';
        }
    };

    const handleClick = (url) => {
        if (url != activeUrl) {
            activeUrl = url;
            if (url != $page.url.pathname) goto(url);
        }
    };
</script>

<div class="flex h-full flex-1 flex-row">
    <div
        id="sidebar"
        class="flex flex-col justify-between p-2 bg-primary-200 dark:bg-primary-800"
        bind:this="{sidebarElem}">
        <div class="flex flex-col gap-3">
            <div class="flex w-full flex-row overflow-hidden whitespace-nowrap">
                <img src="logo-{$theme}.png" class="p-1 w-[35px] h-[35px]" alt="logo" />
                <span class="ml-4 pt-[2px] self-center font-extrabold text-xl dark:text-white">{PUBLIC_APP_NAME}</span>
            </div>
            <div class="flex w-full flex-row justify-end" on:click="{toggleSidebar}" role="presentation">
                <div class="cursor-pointer rounded-lg hover:bg-primary-100 dark:hover:bg-primary-700">
                    <Icon icon="{isOpen ? 'ep:arrow-left-bold': 'ci:hamburger-md'}" class="p-3 w-[35px] h-[35px]" />
                </div>
            </div>
            {#each menuItems as menuItem, index}
                <div
                    id="sidemenuitem-{index}"
                    class="flex w-full cursor-pointer flex-row overflow-hidden whitespace-nowrap rounded-lg hover:bg-primary-100 dark:hover:bg-primary-700"
                    class:item-active="{activeUrl == menuItem.url}"
                    on:click="{(e) => handleClick(menuItem.url)}"
                    role="presentation">
                    <Icon icon="{menuItem.icon}" class="p-1 w-[35px] h-[35px] min-w-[35px] min-h-[35px]" />
                    <span class="ml-4 self-center font-light">{menuItem.name}</span>
                </div>
                {#if !isOpen}
                    <Tooltip class="z-50" triggeredBy="#sidemenuitem-{index}" placement='right'>
                        {menuItem.name}
                    </Tooltip>
                {/if}
            {/each}
        </div>
        <div class="flex flex-row flex-wrap gap-3">
            <div id="user" class="cursor-pointer rounded-lg hover:bg-primary-100 dark:hover:bg-primary-700">
                <Icon icon="hugeicons:user-circle-02" class="p-1 w-[35px] h-[35px]" />
            </div>
            <div
                class="cursor-pointer rounded-lg hover:bg-primary-100 dark:hover:bg-primary-700"
                class:item-active={activeUrl == '/settings'}
                on:click="{(e) => handleClick('/settings')}"
                role="presentation">
                <Icon icon="hugeicons:settings-01" class="p-1 w-[35px] h-[35px]" />
            </div>
            <DarkMode class="text-primary-950 dark:text-primary-400 hover:bg-primary-100 dark:hover:bg-primary-700" />
            <Dropdown
                triggeredBy="#user"
                placement="{isOpen ? 'top-start' : 'right-end'}"
                offset="0"
                containerClass="z-50 border-[1px] !shadow-none font-light bg-primary-200 dark:bg-primary-800 border-primary-300 dark:border-primary-600">
                <DropdownItem defaultClass="!min-w-[150px] px-1">
                    <div class="rounded p-2 hover:bg-primary-100 dark:hover:bg-primary-700">
                        {data.user.uid}
                    </div>
                </DropdownItem>
                <DropdownDivider divClass="my-1 h-px !bg-primary-300 dark:!bg-primary-600" />
                <DropdownItem href="/signout" defaultClass="!min-w-[150px] px-1">
                    <div class="rounded p-2 hover:bg-primary-100 dark:hover:bg-primary-700">Sign out</div>
                </DropdownItem>
            </Dropdown>
        </div>
    </div>
    <div class="w-full overflow-x-auto">
        <slot />
    </div>
</div>

<style lang="postcss">
    #sidebar {
        width: auto;
        min-width: 49px;
        max-width: 49px;
        transition: max-width 0.2s ease-in-out, min-width 0.2s ease-in-out;
    }

    .item-active {
        @apply bg-primary-100 dark:bg-primary-700;
    }
</style>
