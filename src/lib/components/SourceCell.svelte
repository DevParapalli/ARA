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

<div in:fade class="flex w-full gap-1 px-1 py-2 {colors[Number(source.id.at(-1))]} rounded-btn">
    <div class="flex items-center justify-center">
        <!-- <div class="text-[0.5rem] leading-3">{source.id}</div> -->
        <img class="img h-6 w-6" alt="logo of source" src={`/api/image?url=${source.url}`} />
    </div>
    <div>
        <a href={source.url} target="_blank" class="link line-clamp-1 flex w-full text-xs font-bold">
            <p>{source.title.slice(0, 30) || source.url.slice(0, 30)}...</p>
        </a>
        <div class="flex w-full text-xs">
            <p>{source.snippet.slice(0, 30)}...</p>
        </div>
    </div>
</div>

<style lang="postcss">
    p {
        @apply line-clamp-1;
    }
</style>
