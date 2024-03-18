<script>
    export let data;

    $: ({ supabase } = data);
</script>

<div class="w-full flex-col items-center gap-4 p-10">
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
</div>
