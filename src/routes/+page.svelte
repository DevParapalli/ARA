<script>
    export let data;

    $: ({ supabase } = data);
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

<div class="w-full h-full flex flex-col p-5">
    <div class="action-buttons flex flex-row space-x-3">
        <a href="/notebook/new" class="btn btn-primary btn-sm">
            New Notebook
        </a>

        <div class="join">
            <label class="input input-bordered flex items-center gap-2 input-sm">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 opacity-70"><path fill-rule="evenodd" d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z" clip-rule="evenodd" /></svg>
                <input type="text" class="grow outline-none text-xs border-none focus:shadow-none focus:ring-0 placeholder:text-base-content p-0" placeholder="Search" />
            </label>
        </div>
    </div>
</div>