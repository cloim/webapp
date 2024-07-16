<script lang="ts">
    let clazz: string = "";
    export { clazz as class };
    export let directions: string[] = [];
    
    let resizableDiv: HTMLDivElement;

    function resizer(element: HTMLDivElement, _directions: string[]) {
        const grabbers: HTMLDivElement[] = [];

        _directions.forEach(direction => {
            const grabber = document.createElement('div');
            grabber.classList.add('grabber');

            if (direction == "right") {
                grabber.classList.add("right");
            } else if (direction == "left") {
                grabber.classList.add("left");
            }
            grabbers.push(grabber);
        });

        let active: Element | null = null;
        let initialRect: DOMRect | null = null;
        let initialPos: { x: number; y?: number; } | null = null;

        grabbers.forEach(grabber => {
            element.appendChild(grabber);
            grabber.addEventListener('mousedown', onMousedown);
        })

        function onMousedown(event: MouseEvent) {
            if (event.target instanceof Element) {
                active = event.target;
                const rect = element.getBoundingClientRect();
                const parent = element.parentElement?.getBoundingClientRect();

                initialRect = {
                    ...rect,
                    width: rect.width,
                    height: rect.height,
                    left: rect.left - (parent ? parent.left : 0),
                    right: (parent ? parent.right : 0) - rect.right,
                    top: rect.top - (parent ? parent.top : 0),
                    bottom: (parent ? parent.bottom : 0) - rect.bottom,
                };
                initialPos = { x: event.pageX, y: event.pageY };
                active.classList.add('selected');
            }
        }

        function onMouseup(event: MouseEvent) {
            if (!active) return;
            
            active.classList.remove('selected');
            active = null;
            initialRect = null;
            initialPos = null;
            element.style.userSelect = "auto";
        }

        function onMove(event: MouseEvent) {
            if (!active) return;
            if (!initialPos) return;
            if (!initialRect) return;

            const delta = event.pageX - initialPos.x;

            if (active.classList.contains("right")) {
                element.style.width = `${initialRect.width + delta}px`;
            } else if (active.classList.contains("left")) {
                element.style.width = `${initialRect.width - delta}px`;
            }
            element.style.userSelect = "none";
        }

        window.addEventListener('mousemove', onMove);
        window.addEventListener('mouseup', onMouseup);

        return {
            destroy() {
                window.removeEventListener('mousemove', onMove);
                window.removeEventListener('mousemove', onMousedown);
                
                grabbers.forEach(grabber => {
                    element.removeChild(grabber);
                })
            }
        }
    }

    export const setWidth = (w) => {
        resizableDiv.style.width = `${w}px`;
    }
</script>

<div class={`resizable-div ${clazz || ''}`} use:resizer={directions} bind:this={resizableDiv}>
    <slot />
</div>

<style lang="postcss">
    .resizable-div {
        @apply relative overflow-auto;
    }

    :global(.resizable-div .grabber) {
        @apply absolute box-border top-0 w-[5px] h-full cursor-col-resize opacity-0 z-50;
        @apply bg-accent-100;
    }

    :global(.resizable-div .grabber.right) {
        @apply right-0;
    }

    :global(.resizable-div .grabber.left) {
        @apply left-0;
    }

    :global(.resizable-div .grabber.selected) {
		@apply opacity-100;
	}

    :global(.resizable-div .grabber:hover) {
        opacity: 1;
        transition: 0.2s ease-in-out;
    }
</style>