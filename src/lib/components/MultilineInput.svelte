<script lang="ts">
    import { onMount, createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    export let value: string = '';
    export let maxHeight: number = 200;
    export let disabled: boolean = false;

    let textareaElem: HTMLTextAreaElement;

    const autoResize = () => {
        textareaElem.style.height = 'auto';
        textareaElem.style.overflowY = 'hidden';
        textareaElem.style.height = Math.min(textareaElem.scrollHeight, maxHeight) + 'px';

        if (textareaElem.scrollHeight > maxHeight) {
            textareaElem.style.overflowY = 'auto';
        }

        dispatch('input', textareaElem.value);
    };

    onMount(() => {
        autoResize();
    });
</script>

<div class="w-full">
    <textarea class="textarea w-full resize-none" 
        {disabled}
        rows="1" 
        spellcheck="false"
        bind:this="{textareaElem}" 
        bind:value="{value}" 
        on:input="{autoResize}" />
</div>
