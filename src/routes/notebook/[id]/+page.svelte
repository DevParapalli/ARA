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
            infoToast('Connecting...')
            const result = (await ragChain.stream({
                prompt: promptValue,
                context: convert_cells_to_context(cells),
            })) as AsyncGenerator<AIMessageChunk | Object>;
            response = '';
            metadata = {};
            sources = [];
            let citations: any[] = [];
            let status = 0;
            try {
                for await (const chunk of result) {
                    console.debug(chunk);
                    if (chunk instanceof AIMessageChunk) {
                        if ((chunk.content as string).startsWith('__citation__')) {
                            // console.debug('Citation:', chunk);
                            if (typeof chunk.content === 'string' && chunk.content.length > 13)
                                // '__citation__:'
                                citations.push(JSON.parse(chunk.content.slice(13))[0]);
                                if (status == 2) {
                                    infoToast('Citing Sources...');
                                    status = 0;
                                }
                        } else if ((chunk.content as string).startsWith('__search_queries__')) {
                            if (typeof chunk.content === 'string' && chunk.content.length > 19)
                                // '__search_queries__:'
                                Object.assign(metadata, { search_metadata: JSON.parse(chunk.content.slice(19))[0] });
                                if (status == 0) {
                                    infoToast('Deep diving...');
                                    status = 1;
                                }
                        } else if ((chunk.content as string).startsWith('__search_results__')) {
                            if (typeof chunk.content === 'string' && chunk.content.length > 19) {
                                // '__search_results__:'
                                sources = JSON.parse(chunk.content.slice(19)).documents;
                                cells[cell_index].sources = sources;
                            }
                            if (status == 1) {
                                infoToast('Generating content...');
                                status = 2;
                            }
                            // sources.push(chunk);
                        } else if ((chunk.content as string).startsWith('__stream_end__')) {
                            // console.debug('Stream end:', chunk);
                            if (typeof chunk.content === 'string' && chunk.content.length > 15)
                                // '__stream_end__:'
                                Object.assign(metadata, JSON.parse(chunk.content.slice(15)));
                            if (status == 3) {
                                infoToast('Finishing up...');
                                status = 4;
                            }
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
            successToast('RMI Complete!');
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

    let deleting_cell = false;
</script>

<svelte:head>
    <title>Notebook {$page.params.id} | Project ARA</title>
</svelte:head>

<div class="relative flex flex-col items-center p-10">
    {#each cells as cell (cell.id)}
        <div animate:flip class="flex w-full flex-col lg:flex-row">
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
                <CartaEditorCell bind:value={cell.content} />
                <div
                    class="cell-actions flex min-w-32 justify-center rounded-b-box rounded-t-none border border-t-0 border-primary bg-base-300 py-2 xl:min-w-[50%]">
                    <div class="flex w-full items-center justify-evenly gap-4 px-4">
                        <button
                            on:click={() => {
                                if (ai_cell_disabled && conn_status == 'Connected') {
                                    errorToast(
                                        'Cannot modify cells while LLMs are running. Please wait for the LLMs to finish generation.'
                                    );
                                    return;
                                }
                                deleting_cell = true;
                                supabase
                                    .from('cells')
                                    .delete()
                                    .eq('id', cell.id)
                                    .select()
                                    .then(({ data, error }) => {
                                        error ? console.error(error) : dev && console.debug(data);
                                        if (data) {
                                            // cells = cells.filter((c) => c.id !== cell.id);
                                            // const cell_to_remove = cells.findIndex((c) => c.id === cell.id);
                                            cells = cells.filter((c) => c.id !== cell.id);
                                            // this prevents the cell from being upserted as soon as it is deleted
                                            tick().then(() => {
                                                deleting_cell = false;
                                            });
                                        }
                                    });
                            }}
                            class="btn btn-error btn-sm px-1">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 1024 1024"
                                ><path
                                    fill="currentColor"
                                    d="M360 184h-8c4.4 0 8-3.6 8-8zh304v-8c0 4.4 3.6 8 8 8h-8v72h72v-80c0-35.3-28.7-64-64-64H352c-35.3 0-64 28.7-64 64v80h72zm504 72H160c-17.7 0-32 14.3-32 32v32c0 4.4 3.6 8 8 8h60.4l24.7 523c1.6 34.1 29.8 61 63.9 61h454c34.2 0 62.3-26.8 63.9-61l24.7-523H888c4.4 0 8-3.6 8-8v-32c0-17.7-14.3-32-32-32M731.3 840H292.7l-24.2-512h487z" /></svg>
                        </button>

                        <button class="btn btn-ghost btn-sm px-1">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 1024 1024"
                                ><path
                                    fill="currentColor"
                                    d="M758.2 839.1C851.8 765.9 912 651.9 912 523.9C912 303 733.5 124.3 512.6 124C291.4 123.7 112 302.8 112 523.9c0 125.2 57.5 236.9 147.6 310.2c3.5 2.8 8.6 2.2 11.4-1.3l39.4-50.5c2.7-3.4 2.1-8.3-1.2-11.1c-8.1-6.6-15.9-13.7-23.4-21.2a318.64 318.64 0 0 1-68.6-101.7C200.4 609 192 567.1 192 523.9s8.4-85.1 25.1-124.5c16.1-38.1 39.2-72.3 68.6-101.7c29.4-29.4 63.6-52.5 101.7-68.6C426.9 212.4 468.8 204 512 204s85.1 8.4 124.5 25.1c38.1 16.1 72.3 39.2 101.7 68.6c29.4 29.4 52.5 63.6 68.6 101.7c16.7 39.4 25.1 81.3 25.1 124.5s-8.4 85.1-25.1 124.5a318.64 318.64 0 0 1-68.6 101.7c-9.3 9.3-19.1 18-29.3 26L668.2 724a8 8 0 0 0-14.1 3l-39.6 162.2c-1.2 5 2.6 9.9 7.7 9.9l167 .8c6.7 0 10.5-7.7 6.3-12.9z" /></svg>
                        </button>

                        <button class="btn btn-ghost btn-sm px-1">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 1024 1024"
                                ><path
                                    fill="currentColor"
                                    d="M257.7 752c2 0 4-.2 6-.5L431.9 722c2-.4 3.9-1.3 5.3-2.8l423.9-423.9a9.96 9.96 0 0 0 0-14.1L694.9 114.9c-1.9-1.9-4.4-2.9-7.1-2.9s-5.2 1-7.1 2.9L256.8 538.8c-1.5 1.5-2.4 3.3-2.8 5.3l-29.5 168.2a33.5 33.5 0 0 0 9.4 29.8c6.6 6.4 14.9 9.9 23.8 9.9m67.4-174.4L687.8 215l73.3 73.3l-362.7 362.6l-88.9 15.7zM880 836H144c-17.7 0-32 14.3-32 32v36c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-36c0-17.7-14.3-32-32-32" /></svg>
                        </button>
                    </div>
                </div>
            </div>
            {#if cell.type === 'generated' && Array.isArray(cell.sources) && cell.sources.length > 0}
                <div id="sources-container-{cell.id}" class="mx-auto overflow-y-auto p-4 lg:w-[30%]">
                    <span class="lg:hidden">Sources:</span>
                    <div class="flex flex-col items-center gap-y-1">
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
