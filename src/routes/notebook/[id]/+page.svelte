<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
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

    export let data: PageData;
    $: ({ supabase } = data);

    const ragChain = new RemoteRunnable({ url: 'http://localhost:4945/rag' });
    const noragChain = new RemoteRunnable({ url: 'http://localhost:4945/norag' });

    let cells: Tables<'cells'>[] = [];
    onMount(() => {
        (async () => {
            const { data, error } = await supabase
                .from('cells')
                .select('*')
                .eq('notebook', $page.params.id)
                .order('created_at', { ascending: true });
            dev && console.debug(data, error);
            if (data) {
                cells = data;
            } else {
                console.error(error);
            }
        })();

        heartbeat().then((status) => {
            if (status) {
                ai_cell_disabled = false;
            }
        });
        // const interval = setInterval(heartbeat, 20000);
        // return () => {
        //     clearInterval(interval);
        // };
    });

    function handleAddCellUser() {
        supabase
            .from('cells')
            .insert({ notebook: $page.params.id, content: '' })
            .select()
            .single()
            .then(({ data, error }) => {
                error ? console.error(error) : dev && console.debug(data);
                if (data) {
                    cells = [...cells, data];
                }
            });
    }

    let promptValue = '';

    let ai_cell_disabled = true;

    function handleAddCellAI() {
        ai_cell_disabled = true;
        supabase
            .from('cells')
            .insert({
                notebook: $page.params.id,
                type: 'generated',
                content: '',
                metadata: {
                    prompt: promptValue,
                },
            })
            .select()
            .single()
            .then(({ data, error }) => {
                error ? console.error(error) : dev && console.debug(data);
                if (data) {
                    cells = [...cells, data];
                }
            });

        let cell_index = cells.length - 1;

        // let new_cell = { id: 'ABC', notebook: $page.params.id, content: promptValue };
        // cells = [...cells, new_cell];

        const modal = document.getElementById('ai_prompt_modal');
        modal?.close(); // @ts-ignore

        let metadata = {};
        let sources = [];
        let response = '';

        (async (cell_index) => {
            // console.log('Cell index:', cell_index);

            const result = (await ragChain.stream({
                prompt: promptValue,
                context: convert_cells_to_context(cells),
            })) as AsyncGenerator<AIMessageChunk | Object>;
            response = '';
            metadata = {};
            sources = [];
            let citations: any[] = [];
            try {
                for await (const chunk of result) {
                    console.debug(chunk);
                    if (chunk instanceof AIMessageChunk) {
                        if ((chunk.content as string).startsWith('__citation__')) {
                            // console.debug('Citation:', chunk);
                            if (typeof chunk.content === 'string' && chunk.content.length > 13)
                                // '__citation__:'
                                citations.push(JSON.parse(chunk.content.slice(13))[0]);
                        } else if ((chunk.content as string).startsWith('__search_queries__')) {
                            if (typeof chunk.content === 'string' && chunk.content.length > 19)
                                // '__search_queries__:'
                                Object.assign(metadata, { search_metadata: JSON.parse(chunk.content.slice(19))[0] });
                        } else if ((chunk.content as string).startsWith('__search_results__')) {
                            if (typeof chunk.content === 'string' && chunk.content.length > 19)
                                // '__search_results__:'
                                sources = JSON.parse(chunk.content.slice(19)).documents;
                            cells[cell_index].sources = sources;
                            // sources.push(chunk);
                        } else if ((chunk.content as string).startsWith('__stream_end__')) {
                            // console.debug('Stream end:', chunk);
                            if (typeof chunk.content === 'string' && chunk.content.length > 15)
                                // '__stream_end__:'
                                Object.assign(metadata, JSON.parse(chunk.content.slice(15)));
                        } else {
                            response += chunk.content as string;
                            cells[cell_index].content += chunk.content as string;
                        }
                    } else {
                        // console.debug(chunk);
                        Object.assign(metadata, chunk);
                    }
                }
            } catch (error) {
                console.error('Error during retrieval:', error);
            }

            cells[cell_index].metadata = Object.assign(cells[cell_index].metadata || {}, metadata);
            cells[cell_index].sources = sources;
            cells[cell_index].content = response;
            cells[cell_index].citations = citations;
            const { data, error } = await supabase.from('cells').upsert(cells[cell_index]).select().single();
            if (error || !data) {
                console.error(error);
            } else {
                console.debug(data);
                cells[cell_index] = data;
            }
            // finally, free the cell
            ai_cell_disabled = false;
        })(cell_index + 1);

        promptValue = '';
    }

    let conn_status = 'Disconnected';
    let conn_status_flag = 'text-red-500';

    async function heartbeat() {
        try {
            conn_status = 'Connecting...';
            conn_status_flag = 'text-yellow-500';
            await fetch('http://localhost:4945');
            conn_status = 'Connected';
            conn_status_flag = 'text-green-500';

            // set allow for other things...
            // ai_cell_disabled = false;
            return true;
        } catch (e) {
            conn_status = 'Disconnected';
            conn_status_flag = 'text-red-500';
            console.error(e);
            return false;
        }
    }
</script>

<div class="relative flex flex-col items-center p-10">
    {#each cells as cell (cell.id)}
        <div animate:flip class="flex lg:flex-row flex-col w-full">
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
                    supabase
                        .from('cells')
                        .upsert({ id: cell.id, content: cell.content, notebook: $page.params.id })
                        .then(({ data, error }) => {
                            error ? console.error(error) : dev && console.debug(data);
                        });
                }}
                class="flex h-fit w-full flex-col items-center justify-center p-4">
                <CartaEditorCell bind:value={cell.content} />
                <div
                    class="cell-actions flex min-w-32 justify-center rounded-b-box rounded-t-none border border-t-0 border-primary bg-base-300 xl:min-w-[50%]">
                    <div>Cell-level actions.</div>
                </div>
            </div>
            {#if cell.type === 'generated' && Array.isArray(cell.sources) && cell.sources.length > 0}
                <div id="sources-container-{cell.id}" class="lg:w-[30%] mx-auto overflow-y-auto p-4">
                    <span class="lg:hidden">Sources:</span>
                    <div class="flex flex-col gap-y-1 items-center">
                        {#each cell.sources as source}
                            <SourceCell {source} />
                        {/each}
                    </div>
                </div>
            {/if}
        </div>
    {:else}
        <div class="flex flex-col items-center p-10 w-full">
            <div class="skeleton h-96 w-full"></div>
            <div class="skeleton h-6 w-[50%] mb-10"></div>
            <div class="skeleton h-6 w-[50%] mb-10"></div>
            <!-- <div class="skeleton h-4 w-full"></div> -->
            <!-- <div class="skeleton h-4 w-full"></div> -->
        </div>
    {/each}

    {#if supabase && supabase.auth.getSession()}
        <div class="flex flex-row items-center justify-center gap-4">
            <button class="btn btn-primary" on:click={handleAddCellUser}>Add User Cell</button>
            <button
                disabled={ai_cell_disabled}
                class="btn btn-secondary"
                on:click={() => {
                    // ai_cell_disabled = true;
                    const modal = document.getElementById('ai_prompt_modal');
                    modal?.showModal();
                }}>Add AI Cell</button>
        </div>
    {:else}
        <div class="flex w-full flex-row justify-center gap-4">
            <div class="skeleton h-12 w-32"></div>
            <div class="skeleton h-12 w-32"></div>
        </div>
    {/if}

    <dialog id="ai_prompt_modal" class="modal">
        <div class="modal-box">
            <h3 class="pb-4 text-lg font-bold">Enter Prompt</h3>
            <!-- <p class="py-4">Press ESC key or click the button below to close</p> -->
            <input
                type="text"
                placeholder="Give instructions for setting up..."
                class="input input-primary w-full font-mono"
                bind:value={promptValue} />
            <div class="modal-action">
                <form method="dialog">
                    <!-- if there is a button in form, it will close the modal -->
                    <button on:click|preventDefault={handleAddCellAI} class="btn btn-primary w-20">Submit</button>
                    <button
                        on:click={() => {
                            ai_cell_disabled = false;
                        }}
                        class="btn btn-error w-20">Cancel</button>
                </form>
            </div>
        </div>
    </dialog>

    <div class="fixed bottom-0 right-6">
        <span class={conn_status_flag}>{conn_status}</span>
    </div>
</div>
