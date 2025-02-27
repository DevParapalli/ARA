<script lang="ts">
    import { goto, invalidate, invalidateAll } from '$app/navigation';
    import { page } from '$app/stores';
    import type { Database, Tables } from '$lib/supabaseTypes';
    import { errorToast, infoToast } from '$lib/toast';
    import { getRelativeTime } from '$lib/utils';
    import type { SupabaseClient } from '@supabase/supabase-js';
    import toast from 'svelte-french-toast';
    export let notebook: Tables<'notebooks'>;
    export let supabase: SupabaseClient<Database>;
</script>

<a
    href={`/notebook/${notebook.id}`}
    class="aspect-video w-full md:w-auto md:h-64 rounded-box border-2 border-base-content/25 bg-base-200 p-4 transition-colors hover:border-base-content/60 hover:bg-base-100">
    <div class="flex h-full flex-col gap-2">
        <div class="inline-flex items-center justify-between">
            <h2 class="line-clamp-1 text-2xl">{notebook.name}</h2>
            {#if notebook.public}
            <span class="badge badge-warning px-1 py-2">Public</span>
            {/if}
        </div>
        <hr class="my-2 w-full border-base-100 h-fit hidden md:block" />
        {#if typeof notebook.notes === 'object' && notebook.notes !== null && 'field' in notebook.notes}
            <p class="line-clamp-2">{notebook.notes.field}</p>
            <hr class="my-2 w-full border-base-100 hidden md:block" />
        {:else if notebook.notes}
            <p class="line-clamp-2">{notebook.notes}</p>
            <hr class="my-2 w-full border-base-100 hidden md:block" />
        {/if}
        <div class="mt-auto flex flex-row flex-wrap items-center justify-between gap-2">
            <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- <details on:click|stopPropagation={() => {}} class="dropdown dropdown-top">
                <summary class="btn btn-sm items-center justify-center px-0 aspect-square"><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12.005 11.995v.01m0-4.01v.01m0 7.99v.01"/></svg></summary>
                <ul class="p-2 shadow menu dropdown-content z-[1] bg-base-content/10 rounded-box w-52">
                    <li><span on:click|stopPropagation={() => {}}>Delete Notebook</span></li>
                </ul>
            </details> -->

            <a href={`/notebook/${notebook.id}/edit`} class="btn btn-outline btn-accent btn-sm">Edit</a>
            <button
                on:click|preventDefault|stopPropagation={async () => {
                    const { data, error } = await supabase.from('notebooks').delete().eq('id', notebook.id);

                    if (error) {
                        errorToast('Cannot delete notebook. Please remove cells inside.');
                        return;
                    }

                    await invalidateAll();
                    infoToast(`Successfully deleted ${notebook.name}.`)
                    // console.log(await supabase.from('notebooks').delete().eq('id', notebook.id
                }}
                class="btn btn-outline btn-error btn-sm">Delete</button>
            <button on:click|preventDefault|stopPropagation={async () => {
                navigator.clipboard.writeText(`${($page.url.origin)}/notebook/${notebook.id}/view`)
                infoToast('Copied to clipboard.')
                // goto(`${($page.url.origin)}/notebook/${notebook.id}/view`)
            }} class="btn btn-outline btn-secondary btn-sm md:mr-auto">Copy View Link</button>

            <span title={`Created on ${new Date(notebook.created_at).toLocaleString()}`} class="text-xs">created {getRelativeTime(new Date(notebook.created_at))}</span>
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
