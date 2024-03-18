<script>
    import { enhance } from '$app/forms';
    import { fade } from 'svelte/transition';
    export let form;

    let visible = false;
</script>

<div class="mx-auto my-auto flex w-full max-w-md flex-col items-center gap-y-12 rounded-lg bg-base-300 p-8">
    <h2 class="text-4xl">Log in</h2>
    <form action="?/login" method="POST" use:enhance class="form-control items-start gap-2">
        {#if form?.invalid}<div
                transition:fade
                class="flex w-full justify-center rounded-sm bg-error py-1 text-error-content"
            >
                <span>{form?.message}</span>
            </div>{/if}
        <div class="label">
            <label class="label-text" for="email">Email</label>
        </div>
        <input class="input w-full font-mono" name="email" type="email" value={form?.email ?? ''} required />
        <div class="label">
            <label class="label-text" for="password">Password</label>
        </div>
        <div class="join">
            <input class="input join-item font-mono" name="password" type={visible ? 'text' : 'password'} required />
            <button
                on:click|preventDefault={() => {
                    visible = !visible;
                }}
                class="btn btn-ghost bg-base-100"
            >
                {#if visible}
                    <svg xmlns="http://www.w3.org/2000/svg" width="1rem" height="1rem" viewBox="0 0 20 20"
                        ><path
                            fill="currentColor"
                            d="M2.854 2.146a.5.5 0 1 0-.708.708l3.5 3.498a8.097 8.097 0 0 0-3.366 5.046a.5.5 0 1 0 .98.204a7.09 7.09 0 0 1 3.107-4.528L7.953 8.66a3.5 3.5 0 1 0 4.886 4.886l4.307 4.308a.5.5 0 0 0 .708-.708zm9.265 10.68A2.5 2.5 0 1 1 8.673 9.38zm-1.995-4.824l3.374 3.374a3.5 3.5 0 0 0-3.374-3.374M10 6c-.57 0-1.129.074-1.666.213l-.803-.803A7.648 7.648 0 0 1 10 5c3.693 0 6.942 2.673 7.72 6.398a.5.5 0 0 1-.98.204C16.058 8.327 13.207 6 10 6"
                        /></svg
                    >
                {:else}
                    <svg xmlns="http://www.w3.org/2000/svg" width="1rem" height="1rem" viewBox="0 0 20 20"
                        ><path
                            fill="currentColor"
                            d="M3.26 11.602C3.942 8.327 6.793 6 10 6c3.206 0 6.057 2.327 6.74 5.602a.5.5 0 0 0 .98-.204C16.943 7.673 13.693 5 10 5c-3.693 0-6.943 2.673-7.72 6.398a.5.5 0 0 0 .98.204M10 8a3.5 3.5 0 1 0 0 7a3.5 3.5 0 0 0 0-7m-2.5 3.5a2.5 2.5 0 1 1 5 0a2.5 2.5 0 0 1-5 0"
                        /></svg
                    >
                {/if}
            </button>
        </div>

        <button class="btn btn-primary btn-block" type="submit">Login</button>
        <a class="link link-info mr-auto" href="/auth/reset_password">Reset password</a>
    </form>
</div>
