<script lang="ts">
    import type { LCSource } from '$lib/types/langchain';
    import { fade } from 'svelte/transition';

    export let source: LCSource;

    // console.log(source)

    const colors = [
        'bg-red-900',
        'bg-amber-900',
        'bg-lime-900',
        'bg-emerald-900',
        'bg-sky-900',
        'bg-blue-900',
        'bg-violet-900',
        'bg-fuchsia-900',
        'bg-rose-900',
        'bg-slate-900',
    ];
</script>

<div in:fade class="flex justify-evenly w-full gap-1 px-1 py-2 {colors[Number(source.id.at(-1))]} rounded-btn">
    <div class="flex items-center justify-center w-8">
        <!-- <div class="text-[0.5rem] leading-3">{source.id}</div> -->
        <img class="img h-6 w-6" alt="logo of source" src={`/api/image?url=${source.url}`} />
    </div>
    <div class="w-[80%]">
        <a href={source.url} target="_blank" class="link flex text-xs font-bold">
            <p class="line-clamp-1">{source.title || source.url}</p>
        </a>
        <div class="flex w-full text-xs">
            <p class="line-clamp-1">{source.snippet}</p>
        </div>
    </div>
</div>

<style lang="postcss">
    p {
        @apply line-clamp-1;
    }
</style>
