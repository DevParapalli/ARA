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

    export let data: PageData;
    $: ({ supabase } = data);

    // const remoteChain = new RemoteRunnable({ url: 'http://localhost:4945/rag' });
    const remoteChain = new RemoteRunnable({ url: 'http://localhost:4945/norag' });

    let cells: Tables<'cells'>[] = [];
    onMount(() => {
        (async () => {
            const { data, error } = await supabase.from('cells').select('*').eq('notebook', $page.params.id);
            dev && console.log(data, error);
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
        })
        const interval = setInterval(heartbeat, 20000);
        return () => {
            clearInterval(interval);
        };
    });

    function handleAddCellUser() {
        supabase
            .from('cells')
            .insert({ notebook: $page.params.id, content: '' })
            .select()
            .single()
            .then(({ data, error }) => {
                error ? console.error(error) : dev && console.log(data);
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
                    sources: [],
                },
            })
            .select()
            .single()
            .then(({ data, error }) => {
                error ? console.error(error) : dev && console.log(data);
                if (data) {
                    cells = [...cells, data];
                }
            });

        // let new_cell = { id: 'ABC', notebook: $page.params.id, content: promptValue };
        // cells = [...cells, new_cell];

        const modal = document.getElementById('ai_prompt_modal');
        modal?.close();

        let metadata = {};
        let sources = [];
        let response = '';

        (async () => {
            const result = await remoteChain.stream({ prompt: promptValue, context: convert_cells_to_context(cells) });
            console.log("Result", result);
            for await (const chunk of result) {
                if (typeof chunk === 'string') {
                    response += chunk;
                    continue;
                }
                if ('run_id' in (chunk as object) || 'prompt' in (chunk as object) || 'context' in (chunk as object)) {
                    metadata = Object.assign(metadata, chunk);
                } else if ('sources' in (chunk as object)) {
                    sources = chunk as Array<Document>;
                } else if ('response' in (chunk as object)) {
                    response += chunk['response'] as string;
                } else {
                    other = chunk;
                    console.log(chunk);
                }

                cells[cells.length - 1].content += response;
            }

            console.log(metadata, sources, response)
            
            cells[cells.length - 1].metadata = metadata;
            cells[cells.length - 1].metadata.sources = sources;
            cells[cells.length - 1].content = response;
            const {data, error} = await supabase.from('cells').upsert(cells[cells.length - 1]).select().single();
            if (error || !data) {
                console.error(error);
            } else {
                console.log(data);
                cells[cells.length - 1] = data;
            }
        })();

        promptValue = '';
        ai_cell_disabled = false;
    }

    let conn_status = 'Disconnected';
    let conn_status_flag = 'text-redd-500';

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

<div class="flex flex-col items-center p-10 relative">
    {#each cells as cell (cell.id)}
        <div
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
                        error ? console.error(error) : dev && console.log(data);
                    });
            }}
            class="flex flex-col h-fit w-full justify-center items-center p-4"
        >
            <CartaEditorCell bind:value={cell.content} />
        <div class="cell-actions flex justify-center min-w-32 bg-base-300 rounded-t-none rounded-b-box border border-t-0 border-primary">
            <span>XNX</span>
        </div>
        </div>
    {/each}

    <div class="flex flex-row items-center justify-center gap-4">
        <button class="btn btn-primary" on:click={handleAddCellUser}>Add User Cell</button>
        <button
            disabled={ai_cell_disabled}
            class="btn btn-secondary"
            on:click={() => {
                // ai_cell_disabled = true;
                const modal = document.getElementById('ai_prompt_modal');
                modal?.showModal();
            }}>Add AI Cell</button
        >
    </div>

    <dialog id="ai_prompt_modal" class="modal">
        <div class="modal-box">
            <h3 class="pb-4 text-lg font-bold">Enter Prompt</h3>
            <!-- <p class="py-4">Press ESC key or click the button below to close</p> -->
            <input
                type="text"
                placeholder="Give instructions for setting up..."
                class="input input-primary w-full font-mono"
                bind:value={promptValue}
            />
            <div class="modal-action">
                <form method="dialog">
                    <!-- if there is a button in form, it will close the modal -->
                    <button on:click|preventDefault={handleAddCellAI} class="btn btn-primary w-20">Submit</button>
                    <button
                        on:click={() => {
                            ai_cell_disabled = false;
                        }}
                        class="btn btn-error w-20">Cancel</button
                    >
                </form>
            </div>
        </div>
    </dialog>

    <div class="fixed right-6 bottom-0">
        <span class={conn_status_flag}>{conn_status}</span>
    </div>
</div>
