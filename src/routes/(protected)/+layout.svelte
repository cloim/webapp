<script>
    import { PUBLIC_APP_NAME } from '$env/static/public';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { Dropdown, DropdownItem, DropdownDivider, DarkMode } from 'flowbite-svelte';
    import Icon from '@iconify/svelte';
    import logo from '$images/logo.png';
    import { menuItems } from './MenuItems.svelte';

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
            sidebarElem.style.width = '300px';
        } else {
            sidebarElem.style.width = '56px';
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
        class="flex flex-col justify-between bg-neutral-200 p-2 text-neutral-500 dark:bg-neutral-900 dark:text-neutral-400"
        bind:this="{sidebarElem}">
        <div class="flex flex-col gap-3">
            <div class="flex w-full flex-row overflow-hidden whitespace-nowrap p-[6px]">
                <img src={logo} class="w-7 h-7" alt="logo" />
                <span class="ml-4 self-center font-extrabold">{PUBLIC_APP_NAME}</span>
            </div>
            <div class="flex w-full flex-row justify-end" on:click="{toggleSidebar}" role="presentation">
                <div class="cursor-pointer rounded-lg p-[12px] hover:bg-neutral-100 dark:hover:bg-neutral-700">
                    <Icon icon="{isOpen ? 'ep:arrow-left-bold': 'ci:hamburger-md'}" class="h-4 w-4" />
                </div>
            </div>
            {#each menuItems as menuItem}
                <div
                    class="flex w-full cursor-pointer flex-row overflow-hidden whitespace-nowrap rounded-lg p-[6px] hover:bg-neutral-100 dark:hover:bg-neutral-700"
                    class:item-active="{activeUrl == menuItem.url}"
                    on:click="{(e) => handleClick(menuItem.url)}"
                    role="presentation">
                    <Icon icon="{menuItem.icon}" class="h-7 min-h-7 w-7 min-w-7" />
                    <span class="ml-4 self-center font-light">{menuItem.name}</span>
                </div>
            {/each}
        </div>
        <div class="flex flex-row flex-wrap gap-3">
            <div id="user" class="cursor-pointer rounded-lg p-[6px] hover:bg-neutral-100 dark:hover:bg-neutral-700">
                <Icon icon="hugeicons:user-circle-02" class="h-7 min-h-7 w-7 min-w-7" />
            </div>
            <div
                class="cursor-pointer rounded-lg p-[6px] hover:bg-neutral-100 dark:hover:bg-neutral-700"
                class:item-active={activeUrl == '/settings'}
                on:click="{(e) => handleClick('/settings')}"
                role="presentation">
                <Icon icon="hugeicons:settings-01" class="h-7 min-h-7 w-7 min-w-7" />
            </div>
            <DarkMode />
            <Dropdown
                triggeredBy="#user"
                placement="{isOpen ? 'top-start' : 'right-end'}"
                offset="0"
                containerClass="z-50 border-[1px] !border-neutral-300 !bg-neutral-200 !shadow-none dark:!border-black dark:!bg-neutral-900 text-sm font-light">
                <DropdownItem defaultClass="!min-w-[150px] px-1">
                    <div class="rounded p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700">
                        {data.user.uid}
                    </div>
                </DropdownItem>
                <DropdownDivider divClass="my-1 h-px bg-neutral-300 dark:bg-black" />
                <DropdownItem href="/signout" defaultClass="!min-w-[150px] px-1">
                    <div class="rounded p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700">Sign out</div>
                </DropdownItem>
            </Dropdown>
        </div>
    </div>
    <slot />
</div>

<style lang="postcss">
    #sidebar {
        width: 56px;
        transition: width 0.2s ease-in-out;
    }

    .item-active {
        @apply bg-neutral-100;
        @apply dark:bg-neutral-700;
    }
</style>
