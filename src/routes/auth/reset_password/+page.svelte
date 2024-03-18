<script>
    import { enhance } from '$app/forms';
    import { fade } from 'svelte/transition';
    export let form;
</script>

<div class="m-auto flex w-full max-w-md flex-col items-center gap-y-2 rounded-lg bg-base-300 p-8">
    <h2 class="text-4xl">Password Reset</h2>
    <form action="?/reset_password" method="POST" class="form-control items-start gap-2" use:enhance>
        {#if form?.invalid}<div
                transition:fade
                class="flex w-full justify-center rounded-sm bg-error py-1 text-error-content"
            >
                <span>{form?.message}</span>
            </div>{/if}
        <div class="label">
            <label class="label-text" for="email">Email</label>
        </div>
        <input class="input w-full font-mono" type="email" name="email" placeholder="name@domain.com" required />
        <button class="btn btn-primary btn-block" type="submit">Send Link</button>
    </form>
    <!-- {#if form?.invalid}<mark>{form?.message}!</mark>{/if} -->
</div>
