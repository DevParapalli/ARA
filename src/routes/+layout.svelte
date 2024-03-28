<script>
    import '../app.pcss';
    import { enhance } from '$app/forms';
    import { invalidate, invalidateAll, goto, beforeNavigate } from '$app/navigation';
    import { onMount } from 'svelte';

    export let data;

    $: ({ supabase } = data);

    onMount(async () => {
        const _s = await supabase.auth.onAuthStateChange((event, _session) => {
            // If you want to fain grain which routes should rerun their load function
            // when onAuthStateChange changges
            // use invalidate('supabase:auth')
            // which is linked to +layout.js depends('supabase:auth').
            // This should mainly concern all routes
            //that should be accesible only for logged in user.
            // Otherwise use invalidateAll()
            // which will rerun every load function of you app.
            invalidate('supabase:auth');
            invalidateAll();
        });

        const theme = localStorage.getItem('theme') ?? 'dim';
        document.documentElement.setAttribute('data-theme', theme);

        return () => _s.data.subscription.unsubscribe();
    });

    const submitLogout = async ({ cancel }) => {
        const { error } = await data.supabase.auth.signOut();
        if (error) {
            console.debug(error);
        }
        cancel();
        await goto('/');
    };

    let drawer_open = false;

    beforeNavigate(() => {
        drawer_open = false;
        // console.log('drawer_open', drawer_open);
    });
</script>

<div class="drawer h-full lg:drawer-open">
    <input bind:checked={drawer_open} id="sidebar-drawer" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex h-screen w-full flex-col items-center justify-center">
        <div class="w-full overflow-y-auto">
            <slot />
        </div>
    </div>
    <div class="drawer-side">
        <label for="sidebar-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
        <ul class="menu min-h-full w-80 bg-base-200 p-4 text-base-content">
            <!-- Sidebar content here -->
            <li><a href="/">Home</a></li>
            {#if !data.session}
                <li><a href="/auth/login">login</a></li>
                <li><a href="/auth/register">Register</a></li>
            {:else}
                <li><a href="/auth/user_profile">User Profile</a></li>
                <li class="text-error">
                    <form action="/auth/logout?/logout" method="POST" use:enhance={submitLogout}>
                        <button type="submit">Logout &gt;</button>
                    </form>
                </li>

                <a href="/auth/user_profile" class="mt-auto flex w-full items-center gap-4">
                    <div class="flex items-center justify-center rounded-full bg-slate-800 p-4">
                        <svg xmlns="http://www.w3.org/2000/svg" width="1.5rem" height="1.5rem" viewBox="0 0 1200 1200"
                            ><path
                                fill="currentColor"
                                d="M939.574 858.383c-157.341-57.318-207.64-105.702-207.64-209.298c0-62.17 51.555-102.462 69.128-155.744c17.575-53.283 27.741-116.367 36.191-162.256c8.451-45.889 11.809-63.638 16.404-112.532C859.276 157.532 818.426 0 600 0C381.639 0 340.659 157.532 346.404 218.553c4.596 48.894 7.972 66.645 16.404 112.532c8.433 45.888 18.5 108.969 36.063 162.256c17.562 53.286 69.19 93.574 69.19 155.744c0 103.596-50.298 151.979-207.638 209.298C102.511 915.83 0 972.479 0 1012.5V1200h1200v-187.5c0-39.957-102.574-96.606-260.426-154.117" /></svg>
                    </div>
                    <div class="text-sm">{data.session.user.email}</div>
                </a>
                <!-- TODO: Update Links -->
            {/if}
        </ul>
    </div>
</div>

<label for="sidebar-drawer" class="btn btn-primary drawer-button absolute bottom-0 right-0 mb-6 mr-6 lg:hidden"
    >MENU</label>

<style>
    form {
        display: inline;
    }
</style>
