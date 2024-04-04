<script lang="ts">
    import type { PageData } from './$types';

    import NotebookHomeComponent from '$lib/components/NotebookHomeComponent.svelte';
    import { invalidate } from '$app/navigation';
    import { flip } from 'svelte/animate';
    import { fade } from 'svelte/transition';
    import type { Tables } from '$lib/supabaseTypes';

    export let data: PageData;

    $: ({ supabase } = data);

    let filteredNotebooks: Tables<'notebooks'>[]

    if (data.data)  
        filteredNotebooks = data.data;

    let searchValue = '';

    $: (data.data && searchValue) ? filteredNotebooks = data.data.filter((notebook) => notebook.name?.toLowerCase().includes(searchValue.toLowerCase())): filteredNotebooks = data.data;
    

    
</script>

<svelte:head>
    <title>Dashboard | Project ARA</title>
</svelte:head>
<!-- <div class="w-full flex-col items-center gap-4 p-10">
    <h1 class="text-6xl">Notebooks</h1>

    {#if data.data}
        {#each data.data as nb}
            {#if nb}
                <a href="/notebook/{nb.id}" class="text-2xl">{nb.name}</a>
            {/if}
        {/each}
    {:else}
        <p>No notebooks found</p>
    {/if}

    <button class="btn btn-primary">
        <a href="notebook/new">New notebook</a>
    </button>
</div> -->
{#if data.data}
<div class="flex h-full w-full flex-col p-5">
    <div class="action-buttons flex flex-row w-full gap-x-3">
        <a href="/notebook/new" class="btn btn-primary btn-sm"> New Notebook </a>

        <div class="join">
            <label class="input input-sm input-bordered flex items-center gap-2">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 16 16"
                    fill="currentColor"
                    class="h-4 w-4 opacity-70"
                    ><path
                        fill-rule="evenodd"
                        d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
                        clip-rule="evenodd" /></svg>
                <input
                    type="text"
                    class="grow border-none p-0 text-xs outline-none placeholder:text-base-content focus:shadow-none focus:ring-0"
                    placeholder="Search" bind:value={searchValue} />
            </label>
        </div>
        
    </div>
    <h1 class="mx-auto text-6xl">Notebooks</h1>

    <div class="flex flex-wrap justify-center gap-4 p-10 lg:items-start lg:justify-normal">
        {#if filteredNotebooks}
            {#each filteredNotebooks as notebook, i (notebook.id)}
                <div transition:fade class="contents">
                    <NotebookHomeComponent {notebook} {supabase} />
                </div>
            {:else}
            <div class="w-full flex-col items-center gap-4 p-10"><p>No notebooks found. Use the button above to create a new one.</p></div>
            {/each}
        {/if}

        <!-- <button on:click={() => {invalidate('')}}>INVALID</button> -->
    </div>
</div>
{:else}
<div class="flex max-w-[100vw] flex-col items-center justify-start xl:flex-row xl:items-start xl:justify-between">
    <div class="shrink xl:w-1/2">
        <div
            class="flex xl:min-h-screen items-center justify-center px-2 py-10 text-center xl:justify-start xl:pe-0 xl:ps-10 xl:text-start">
            <div>
                <div class="h-4" />
                <h1
                class="font-title [:root[dir=rtl]_&amp;]:leading-[1.35] text-center text-[clamp(2rem,6vw,4.2rem)] font-black leading-[1.1] [word-break:auto-phrase] xl:w-[115%] xl:text-start">
                <span
                    class="[&amp;::selection]:text-base-content [&amp;::selection]:bg-blue-700/20 brightness-150 contrast-150"
                    >The most powerful</span> <br />
                <span class="inline-grid"
                    ><span
                        class="pointer-events-none col-start-1 row-start-1 bg-[linear-gradient(90deg,theme(colors.error)_0%,theme(colors.secondary)_9%,theme(colors.secondary)_42%,theme(colors.primary)_47%,theme(colors.accent)_100%)] bg-clip-text blur-xl [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] before:content-[attr(data-text)] [@supports(color:oklch(0%_0_0))]:bg-[linear-gradient(90deg,oklch(var(--s))_4%,color-mix(in_oklch,oklch(var(--s)),oklch(var(--er)))_22%,oklch(var(--p))_45%,color-mix(in_oklch,oklch(var(--p)),oklch(var(--a)))_67%,oklch(var(--a))_100.2%)]"
                        aria-hidden="true"
                        data-text="Research Assistant"></span>
                    <span
                        class="[&amp;::selection]:text-base-content [&amp;::selection]:bg-blue-700/20 relative col-start-1 row-start-1 bg-[linear-gradient(90deg,theme(colors.error)_0%,theme(colors.secondary)_9%,theme(colors.secondary)_42%,theme(colors.primary)_47%,theme(colors.accent)_100%)] bg-clip-text [-webkit-text-fill-color:transparent] [@supports(color:oklch(0%_0_0))]:bg-[linear-gradient(90deg,oklch(var(--s))_4%,color-mix(in_oklch,oklch(var(--s)),oklch(var(--er)))_22%,oklch(var(--p))_45%,color-mix(in_oklch,oklch(var(--p)),oklch(var(--a)))_67%,oklch(var(--a))_100.2%)]"
                        >Research Assistant</span
                    ></span> <br />
                <span
                    class="[&amp;::selection]:text-base-content [&amp;::selection]:bg-blue-700/20 brightness-150 contrast-150"
                    >ever.</span>
            </h1>
            <div class="h-4" />
            <p class="text-base-content/70 font-title py-4 font-light md:text-lg xl:text-xl text-justify px-4">
                Enriching exploration, one prompt at a time.
            </div>
        </div>
    </div>
    <div class="w-full xl:w-1/2 shrink">
        <div class="grid min-h-screen grid-cols-3 grid-rows-3 gap-6 p-2 xl:py-10">
            <div
                class="col-span-2 h-full w-full rounded-box border-2 border-base-content/30 bg-base-200 hover:border-base-content/60 p-4">
                Documents
            </div>
            <div
                class="row-span-2 h-full w-full rounded-box border-2 border-base-content/30 bg-base-200 hover:border-base-content/60 p-4">
                Projects
            </div>
            <div
                class="central h-full w-full rounded-box border-2 border-base-content/30 bg-base-200 hover:border-base-content/60 p-4">
                Community
            </div>
            <div
                class="row-span-2 h-full w-full rounded-box border-2 border-base-content/30 bg-base-200 hover:border-base-content/60 p-4">
                Achievements
            </div>
            <div
                class="col-span-2 h-full w-full rounded-box border-2 border-base-content/30 bg-base-200 hover:border-base-content/60 p-4">
                Competitions
            </div>
        </div>
    </div>
</div>
{/if}


<style>
    * {
        @apply transition-colors duration-300;
    }
    .central {
        grid-column: 2/3;
        grid-row: 2/3;
    }
</style>