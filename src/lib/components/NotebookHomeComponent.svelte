<script lang="ts">
    import type {Tables} from '$lib/supabaseTypes'
    import {getRelativeTime} from '$lib/utils'
    export let notebook: Tables<'notebooks'>;

    
</script>

<a href={`/notebook/${notebook.id}`} class="aspect-[9/16] w-64 rounded-box p-4 border-2 border-base-content/25 hover:border-base-content/60 bg-base-200 hover:bg-base-100 transition-colors ">
    <div class="flex flex-col h-full gap-2">
        <div class="inline-flex items-center justify-between">
            <h2 class="text-2xl line-clamp-1">{notebook.name}</h2>
            <span class="badge badge-warning px-1 py-2 ">Public</span>
        </div>
        <hr class="w-full border-base-100 my-2">
        {#if typeof notebook.notes === 'object' && notebook.notes !== null && 'field' in notebook.notes}
             <p class="line-clamp-2">{notebook.notes.field}</p>
        {:else if notebook.notes !== null}
            <p class="line-clamp-2">{notebook.notes}</p>
        {/if}
        <hr class="w-full border-base-100 my-2">
        <div class="flex flex-row items-center justify-between gap-2 mt-auto">
            <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- <details on:click|stopPropagation={() => {}} class="dropdown dropdown-top">
                <summary class="btn btn-sm items-center justify-center px-0 aspect-square"><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12.005 11.995v.01m0-4.01v.01m0 7.99v.01"/></svg></summary>
                <ul class="p-2 shadow menu dropdown-content z-[1] bg-base-content/10 rounded-box w-52">
                    <li><span on:click|stopPropagation={() => {}}>Delete Notebook</span></li>
                </ul>
            </details> -->

            <a href={`/notebook/${notebook.id}/edit`} class="btn btn-xs btn-outline">Edit</a>
            <button on:click|preventDefault|stopPropagation={() => {}} class="btn btn-xs btn-outline mr-auto">Delete</button>

            <span class="text-xs">created {getRelativeTime(new Date(notebook.created_at))}</span>
        </div>
    </div>
</a>

<!--  
    <details class="dropdown">
  <summary class="m-1 btn">open or close</summary>
  <ul class="p-2 shadow menu dropdown-content z-[1] bg-base-100 rounded-box w-52">
    <li><a>Item 1</a></li>
    <li><a>Item 2</a></li>
  </ul>
</details> -->