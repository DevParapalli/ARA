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

    let cells: Tables<'cells'>[] = [];
    onMount(() => {
        document.getElementById('runner-selector-modal')?.showModal();

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
            infoToast('Connecting...');
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

    let conn_status = false;
    // let conn_status_flag = 'text-red-500';

    async function heartbeat() {
        try {
            // conn_status = 'Connecting...';
            // conn_status_flag = 'text-yellow-500';
            await fetch(heartbeat_url);
            conn_status = true;
            // conn_status_flag = 'text-green-500';

            // set allow for other things...
            // ai_cell_disabled = false;
            return true;
        } catch (e) {
            conn_status = false;
            // conn_status_flag = 'text-red-500';
            console.error(e);
            // ai_cell_disabled = true;
            errorToast('Connection to the server lost. Please reconnect');
            return false;
        }
    }

    let cell_index_to_rewrite = -1;
    let rewrite_prompt = '';

    async function handle_rewriting_cell(content: string, action: string) {
        if (cell_index_to_rewrite == -1) {
            errorToast('Error with Cell Connection');
            return;
        }
        ai_cell_disabled = true;

        let cell_index = -1;

        infoToast('Connecting...');

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
                    cell_index = cells.findIndex((c) => c.id === data.id);
                }
            });

        // let new_cell = { id: 'ABC', notebook: $page.params.id, content: promptValue };
        // cells = [...cells, new_cell];

        const modal = document.getElementById('rewrite-prompt-modal');
        modal?.close(); // @ts-ignore

        let metadata = {};
        let sources = [];
        let response = '';

        const result = await noragChain.stream({
            prompt: `${content}\n\n${action}`,
            context: '',
        });

        response = '';
        metadata = {};
        sources = [];

        infoToast('Generating Content...');

        infoToast('Understanding...', {
            duration: 5000,
        });

        for await (const chunk of result) {
            if (typeof chunk === 'string') {
                response += chunk;
                cells[cell_index].content += chunk as string;
                continue;
            }
            if ('run_id' in (chunk as object) || 'prompt' in (chunk as object) || 'context' in (chunk as object)) {
                metadata = Object.assign(metadata, chunk);
            } else if ('sources' in (chunk as object)) {
                sources = chunk as Array<object>;
            } else if ('response' in (chunk as object)) {
                response += chunk['response'] as string;
                cells[cell_index].content += chunk.response as string;
            } else {
                // other.merge(chunk);
                console.debug(chunk);
            }
        }

        cells[cell_index].metadata = Object.assign(cells[cell_index].metadata || {}, metadata);
        cells[cell_index].sources = sources;
        cells[cell_index].content = response;
        const { data, error } = await supabase.from('cells').upsert(cells[cell_index]).select().single();

        if (error || !data) {
            console.error(error);
        } else {
            console.debug(data);
            cells[cell_index] = data;
        }
        // Remote Model Invocation
        successToast('RMI Complete!');

        ai_cell_disabled = false;
    }

    let deleting_cell = false;
</script>

<svelte:head>
    <title>Notebook {$page.params.id} | Project ARA</title>
</svelte:head>

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
            This notebook contains no cells, use the buttons below to create the first cell
            <div class="skeleton h-96 w-full"></div>
            <div class="skeleton h-6 w-[50%] mb-10"></div>
            <div class="skeleton h-6 w-[50%] mb-10"></div>
            <!-- <div class="skeleton h-4 w-full"></div> -->
            <!-- <div class="skeleton h-4 w-full"></div> -->
        </div>
    {/each}



</div>
