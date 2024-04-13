<script lang="ts">
    import { page } from '$app/stores';
    import { onMount, tick } from 'svelte';
    import type { PageData } from './$types';
    // import CartaViewerCell from '$lib/components/CartaViewerCell.svelte';
    import type { Tables } from '$lib/supabaseTypes';
    import CartaEditorCell from '$lib/components/CartaEditorCell.svelte';
    // import CartaEditorCell from '$lib/components/CartaViewerCell.svelte';
    import { dev } from '$app/environment';
    import { convert_cells_to_context } from '$lib/utils';
    import { RemoteRunnable } from '@langchain/core/runnables/remote';
    import type { RemoteRunnableResponseChunk } from '$lib/types/langchain';
    import { AIMessageChunk } from '@langchain/core/messages';
    import SourceCell from '$lib/components/SourceCell.svelte';
    import { flip } from 'svelte/animate';
    import { errorToast, infoToast, successToast } from '$lib/toast';
    import { fade, slide } from 'svelte/transition';
    import CartaViewerCell from '$lib/components/CartaViewerCell.svelte';

    export let data: PageData;
    $: ({ supabase } = data);

    let ragChain = new RemoteRunnable({ url: 'http://localhost:4945/rag' });
    let noragChain = new RemoteRunnable({ url: 'http://localhost:4945/norag' });
    let heartbeat_url = 'http://localhost:4945';
    // let runner_choice = 'local';

    let cells: Tables<'cells'>[] = data.cells;
    onMount(() => {


        // heartbeat().then((status) => {
        //     if (status) {
        //         ai_cell_disabled = false;
        //     }
        // });
        // const interval = setInterval(heartbeat, 20000);
        // return () => {
        //     clearInterval(interval);
        // };
    });

    let deleting_cell = false;
</script>

<svelte:head>
    <title>Notebook {$page.params.id} | Project ARA</title>
</svelte:head>

<h1 class="mx-auto text-6xl mt-4 text-center">{data.info?.name}</h1>
<h2 class="mx-auto text-xl mt-8 md:mt-4 text-center">{data.info?.notes}</h2>

<div class="relative flex flex-col items-center p-10">
    {#each cells as cell (cell.id)}
        <div in:fade class="flex w-full flex-col lg:flex-row">
            <div
                id="cell-container-{cell.id}"
                on:focusout={(e) => {
                    //@ts-ignore
                    if (e.currentTarget.contains(e.relatedTarget)) {
                        return;
                    }
                    if (cell.id === undefined) {
                        return;
                    } // prevent test cell from updating
                    if (!deleting_cell) {
                        supabase
                            .from('cells')
                            .upsert({ id: cell.id, content: cell.content, notebook: $page.params.id })
                            .then(({ data, error }) => {
                                error ? console.error(error) : dev && console.debug(data);
                            });
                    }
                }}
                class="flex h-fit w-full flex-col items-center justify-center p-4">
                <CartaViewerCell bind:value={cell.content} />
            </div>
            {#if cell.type === 'generated' && Array.isArray(cell.sources) && cell.sources.length > 0}
                <div id="sources-container-{cell.id}" class="mx-auto w-full overflow-y-auto p-4 lg:w-[30%]">
                    <span class="lg:hidden">Sources:</span>
                    <div class="flex flex-col items-center gap-y-1">
                        {#each cell.sources as source, i}
                            <div in:fade={{delay: i * 100}} class="contents">
                                <SourceCell {source} />
                            </div>
                        {/each}
                    </div>
                </div>
            {/if}
        </div>
    {:else}
        <div class="flex flex-col items-center p-10 w-full">
            There is something wrong with this link, ask the sender to recheck.
            <div class="skeleton h-96 w-full"></div>
            <div class="skeleton h-6 w-[50%] mb-10"></div>
            <div class="skeleton h-6 w-[50%] mb-10"></div>
            <!-- <div class="skeleton h-4 w-full"></div> -->
            <!-- <div class="skeleton h-4 w-full"></div> -->
        </div>
    {/each}



</div>
