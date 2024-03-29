<script>
    import { enhance } from '$app/forms';
    import { fade } from 'svelte/transition';
    export let form;
</script>

<div class="flex h-full w-full items-center justify-center">
    <div class="mx-auto my-auto flex w-full max-w-md flex-col items-center rounded-lg bg-base-200 p-4">
        <h2 class="mr-auto text-3xl">Create a new notebook</h2>
        <hr class="mb-4 mt-4 w-full border-base-100" />
        <form action="?/create" method="POST" use:enhance class="form-control items-start gap-2">
            {#if form?.invalid}
                <div transition:fade class="flex w-full justify-center rounded-sm bg-error py-1 text-error-content">
                    <span>{form?.message}</span>
                </div>{/if}
            <div class="text-sm">
                Each notebook is used as its own source, and used for inference. <span class="font-bold">DO NOT</span> mix different types of notes in the same notebook.
            </div>
            <hr class="w-full border-base-100 my-2">
            <div class="label">
                <label class="label-text" for="email">Name</label>
            </div>
            <input class="input w-full font-mono" name="email" type="email" value={form?.email ?? ''} required />
            <div class="label">
                <label class="label-text" for="password">Additional Notes</label>
            </div>
            
                <input
                    class="input w-full font-mono"
                    name="notes"
                    type='text' />
            
            <hr class="w-full border-base-100 my-2">

            <div class="flex w-full justify-between mt-2">
                <a href='/' class="btn btn-outline btn-sm">Cancel</a>
                <button class="btn btn-primary btn-sm" type="submit">Create</button>
                <!-- <a class="link link-info mr-auto" href="/auth/reset_password">Reset password</a> -->
            </div>
        </form>
    </div>
</div>
