<script lang="ts">
    import { enhance } from '$app/forms';
    import { fade } from 'svelte/transition';
    import type { PageData } from './$types';
    export let form;
    export let data: PageData;

    $: ({ supabase, session } = data);
</script>

<svelte:head>
    <title>Create New Notebook | Project ARA</title>
</svelte:head>

<div class="flex h-full w-full items-center justify-center">
    <div class="mx-auto my-auto flex w-full max-w-md flex-col items-center rounded-lg bg-base-200 p-4">
        <h2 class="mr-auto text-3xl">Create a new notebook</h2>
        <hr class="mb-4 mt-4 w-full border-base-100" />
        <form action="?/create" method="POST" use:enhance class="form-control items-start gap-2">
            {#if form?.error}
                <div transition:fade class="flex w-full justify-center rounded-sm bg-error py-1 text-error-content">
                    <span>{form?.message}</span>
                </div>{/if}
            <div class="text-justify text-sm">
                Each notebook is used as its own source, and used for inference. <span class="font-bold">DO NOT</span>
                mix different topics in the same notebook.
                <ul class="text-sm">
                    <li class="list-item">- Name should be greater than 5 characters, and less than 128 characters.</li>
                    <li class="list-item">- Notes field is optional.</li>
                    <li class="list-item">- Notes should be less than 1024 characters.</li>
                </ul>
            </div>
            <hr class="my-2 w-full border-base-100" />
            <div class="label">
                <label class="label-text" for="name">Name</label>
            </div>
            <input
                class="input {form?.error_on == 'name' ? 'input-error' : ''} w-full font-mono"
                name="name"
                type="name"
                value={form?.name ?? ''}
                required />
            <div class="label">
                <label class="label-text" for="notes">Additional Notes</label>
            </div>

            <input
                class="input {form?.error_on == 'notes' ? 'input-error' : ''} w-full font-mono"
                name="notes"
                type="text" />

            <hr class="my-2 w-full border-base-100" />
            <input type="hidden" name="user_id" value={session?.user.id} />
            <div class="mt-2 flex w-full justify-between">
                <a href="/" class="btn btn-outline btn-sm">Cancel</a>
                <button class="btn btn-primary btn-sm" type="submit">Create</button>
                <!-- <a class="link link-info mr-auto" href="/auth/reset_password">Reset password</a> -->
            </div>
        </form>
    </div>
</div>
