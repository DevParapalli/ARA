<script lang="ts">
    import type { PageData } from "./$types";

    import NotebookHomeComponent from "$lib/components/NotebookHomeComponent.svelte";
    import { invalidate } from "$app/navigation";
    import { flip } from "svelte/animate";
    import { fade } from "svelte/transition";


    export let data: PageData;

    $: ({ supabase, data: notebooks } = data);
</script>

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

<div class="flex h-full w-full flex-col p-5">
    <div class="action-buttons flex flex-row space-x-3">
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
                    placeholder="Search" />
            </label>
        </div>
    </div>

    <div class="flex flex-wrap justify-center lg:justify-normal lg:items-start gap-4 p-10">
        {#if data.data}
            {#each data.data as notebook, i (notebook.id)}
                <div transition:fade class="contents">
                    <NotebookHomeComponent {notebook} {supabase} />
                </div>
            {/each}
        {/if}
        <!-- <button on:click={() => {invalidate('')}}>INVALID</button> -->
    </div>
</div>
