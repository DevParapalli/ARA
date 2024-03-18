<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import type { PageData } from './$types';
    import CartaViewerCell from '$lib/components/CartaViewerCell.svelte';
    import type { Tables } from '$lib/supabaseTypes';
    import CartaEditorCell from '$lib/components/CartaEditorCell.svelte';
    import { dev } from '$app/environment';

    export let data: PageData;
    $: ({ supabase } = data);

    let cells: Tables<'cells'>[] = [];
    onMount(async () => {
        const { data, error } = await supabase.from('cells').select('*').eq('notebook', $page.params.id);
        dev && console.log(data, error);
        if (data) {
            cells = data;
        } else {
            console.error(error);
        }
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

    function handleAddCellAI() {
        supabase
            .from('cells')
            .insert({ notebook: $page.params.id, content: promptValue })
            .select()
            .single()
            .then(({ data, error }) => {
                error ? console.error(error) : dev && console.log(data);
                if (data) {
                    cells = [...cells, data];
                }
            });

        const modal = document.getElementById('ai_prompt_modal');
        modal?.close();

        promptValue = '';
    }
</script>

<div class="flex flex-col items-center p-10">
    {#each cells as cell}
        <div
            on:focusout={(e) => {
                //@ts-ignore
                if (e.currentTarget.contains(e.relatedTarget)) {
                    return;
                }
                supabase
                    .from('cells')
                    .upsert({ id: cell.id, content: cell.content, notebook: $page.params.id })
                    .then(({ data, error }) => {
                        error ? console.error(error) : dev && console.log(data);
                    });
            }}
            class="flex w-full justify-center p-4"
        >
            <CartaEditorCell bind:value={cell.content} />
        </div>
    {/each}

    <div class="flex flex-row items-center justify-center gap-4">
        <button class="btn btn-primary" on:click={handleAddCellUser}>Add User Cell</button>
        <button
            class="btn btn-secondary"
            on:click={() => {
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
                    <button on:click|preventDefault={() => {}} class="btn btn-primary w-20">Submit</button>
                    <button class="btn btn-error w-20">Cancel</button>
                </form>
            </div>
        </div>
    </dialog>
</div>
