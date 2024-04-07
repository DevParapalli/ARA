<script lang="ts">
    import '../app.pcss';
    import { enhance } from '$app/forms';
    import { invalidate, invalidateAll, goto, beforeNavigate } from '$app/navigation';
    import { onMount, tick } from 'svelte';
    import toast, { Toaster } from 'svelte-french-toast';
    import { infoToast, normalToast, successToast } from '$lib/toast';
    export let data;

    $: ({ supabase } = data);

    let user_id: string;

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
            if (event == 'SIGNED_OUT') {
                infoToast('Deauthenticated');
            } else if (event == 'SIGNED_IN') {
                successToast('Authenticated');
            } else if (event == 'INITIAL_SESSION') {
                infoToast('Found existing session');
                if (_session) {
                    successToast('Authenticated');
                }
            }

            user_id = _session?.user.id ?? '';
            if (user_id) {
                supabase
                .from('users')
                .select('theme')
                .eq('id', user_id)
                .single()
                .then(({ data, error }) => {
                    if (error) {
                        console.error(error);
                    } else {
                        localStorage.setItem('theme', data.theme || '');
                        // console.log('theme', data);
                        document.documentElement.setAttribute('data-theme', data.theme || '');
                    }
                });
            }
            invalidate('supabase:auth');
            invalidateAll();
        });

        const localTheme = localStorage.getItem('theme') || 'luxury';
        if (localTheme) {
            // console.log('localTheme', localTheme);
            document.documentElement.setAttribute('data-theme', localTheme);
        }

        normalToast('Welcome to the app!', { icon: '👏' });

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
        <div class="h-full w-full overflow-y-auto bg-base-300">
            <slot />
        </div>
    </div>
    <div class="drawer-side border-base-100 lg:border-r-2">
        <label for="sidebar-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
        <ul class="menu min-h-full w-80 bg-base-300 p-4 text-base-content">
            <!-- Sidebar content here -->
            <li class="flex items-center"><button on:click={() => {
                tick().then(() => {
                    goto('/')
                })
            }} on:dblclick={() => {
                goto('/test');
            }} class="font-dune text-6xl">ARA</button></li>
            <hr class="border-base-content/30 my-4">
            <li><a on:dblclick|preventDefault={(e) => goto('/home/')} class="inline-flex items-center text-xl" href="/"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 1024 1024"><path fill="currentColor" d="M946.5 505L560.1 118.8l-25.9-25.9a31.5 31.5 0 0 0-44.4 0L77.5 505a63.9 63.9 0 0 0-18.8 46c.4 35.2 29.7 63.3 64.9 63.3h42.5V940h691.8V614.3h43.4c17.1 0 33.2-6.7 45.3-18.8a63.6 63.6 0 0 0 18.7-45.3c0-17-6.7-33.1-18.8-45.2M568 868H456V664h112zm217.9-325.7V868H632V640c0-22.1-17.9-40-40-40H432c-22.1 0-40 17.9-40 40v228H238.1V542.3h-96l370-369.7l23.1 23.1L882 542.3z"/></svg>Home</a></li>
            {#if !data.session}
                <li><a class="inline-flex items-center text-xl" href="/auth/login"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 1024 1024"><path fill="currentColor" d="M521.7 82c-152.5-.4-286.7 78.5-363.4 197.7c-3.4 5.3.4 12.3 6.7 12.3h70.3c4.8 0 9.3-2.1 12.3-5.8c7-8.5 14.5-16.7 22.4-24.5c32.6-32.5 70.5-58.1 112.7-75.9c43.6-18.4 90-27.8 137.9-27.8c47.9 0 94.3 9.3 137.9 27.8c42.2 17.8 80.1 43.4 112.7 75.9c32.6 32.5 58.1 70.4 76 112.5C865.7 417.8 875 464.1 875 512c0 47.9-9.4 94.2-27.8 137.8c-17.8 42.1-43.4 80-76 112.5s-70.5 58.1-112.7 75.9A352.8 352.8 0 0 1 520.6 866c-47.9 0-94.3-9.4-137.9-27.8A353.84 353.84 0 0 1 270 762.3c-7.9-7.9-15.3-16.1-22.4-24.5c-3-3.7-7.6-5.8-12.3-5.8H165c-6.3 0-10.2 7-6.7 12.3C234.9 863.2 368.5 942 520.6 942c236.2 0 428-190.1 430.4-425.6C953.4 277.1 761.3 82.6 521.7 82M395.02 624v-76h-314c-4.4 0-8-3.6-8-8v-56c0-4.4 3.6-8 8-8h314v-76c0-6.7 7.8-10.5 13-6.3l141.9 112a8 8 0 0 1 0 12.6l-141.9 112c-5.2 4.1-13 .4-13-6.3"/></svg>Login </a></li>
                <li><a class="text-xl inline-flex items-center" href="/auth/register"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="currentColor" d="M15 4a4 4 0 0 0-4 4a4 4 0 0 0 4 4a4 4 0 0 0 4-4a4 4 0 0 0-4-4m0 1.9a2.1 2.1 0 1 1 0 4.2A2.1 2.1 0 0 1 12.9 8A2.1 2.1 0 0 1 15 5.9M4 7v3H1v2h3v3h2v-3h3v-2H6V7zm11 6c-2.67 0-8 1.33-8 4v3h16v-3c0-2.67-5.33-4-8-4m0 1.9c2.97 0 6.1 1.46 6.1 2.1v1.1H8.9V17c0-.64 3.1-2.1 6.1-2.1"/></svg>Register</a></li>
            {:else}
                <!-- <li><a href="/auth/user_profile">User Profile</a></li> -->
                <!-- <li class="text-error">
                    <form action="/auth/logout?/logout" method="POST" use:enhance={submitLogout}>
                        <button type="submit">Logout &gt;</button>
                    </form>
                </li> -->

                <a href="/auth/user_profile" class="mt-auto flex w-full items-center gap-4">
                    <div class="flex items-center justify-center rounded-full bg-slate-800 p-4">
                        <svg xmlns="http://www.w3.org/2000/svg" width="1.5rem" height="1.5rem" viewBox="0 0 1200 1200"
                            ><path
                                fill="currentColor"
                                d="M939.574 858.383c-157.341-57.318-207.64-105.702-207.64-209.298c0-62.17 51.555-102.462 69.128-155.744c17.575-53.283 27.741-116.367 36.191-162.256c8.451-45.889 11.809-63.638 16.404-112.532C859.276 157.532 818.426 0 600 0C381.639 0 340.659 157.532 346.404 218.553c4.596 48.894 7.972 66.645 16.404 112.532c8.433 45.888 18.5 108.969 36.063 162.256c17.562 53.286 69.19 93.574 69.19 155.744c0 103.596-50.298 151.979-207.638 209.298C102.511 915.83 0 972.479 0 1012.5V1200h1200v-187.5c0-39.957-102.574-96.606-260.426-154.117" /></svg>
                    </div>
                    <div class="text-sm inline-flex gap-2 items-center">{data.session.user.email} <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 1024 1024"><path fill="currentColor" d="M574 665.4a8.03 8.03 0 0 0-11.3 0L446.5 781.6c-53.8 53.8-144.6 59.5-204 0c-59.5-59.5-53.8-150.2 0-204l116.2-116.2c3.1-3.1 3.1-8.2 0-11.3l-39.8-39.8a8.03 8.03 0 0 0-11.3 0L191.4 526.5c-84.6 84.6-84.6 221.5 0 306s221.5 84.6 306 0l116.2-116.2c3.1-3.1 3.1-8.2 0-11.3zm258.6-474c-84.6-84.6-221.5-84.6-306 0L410.3 307.6a8.03 8.03 0 0 0 0 11.3l39.7 39.7c3.1 3.1 8.2 3.1 11.3 0l116.2-116.2c53.8-53.8 144.6-59.5 204 0c59.5 59.5 53.8 150.2 0 204L665.3 562.6a8.03 8.03 0 0 0 0 11.3l39.8 39.8c3.1 3.1 8.2 3.1 11.3 0l116.2-116.2c84.5-84.6 84.5-221.5 0-306.1M610.1 372.3a8.03 8.03 0 0 0-11.3 0L372.3 598.7a8.03 8.03 0 0 0 0 11.3l39.6 39.6c3.1 3.1 8.2 3.1 11.3 0l226.4-226.4c3.1-3.1 3.1-8.2 0-11.3z"/></svg></div>
                </a>
                <li class="btn btn-error btn-sm px-1 mt-4">
                    <form action="/auth/logout?/logout" method="POST" use:enhance={submitLogout}>
                        <button class="inline-flex items-center gap-2" type="submit">Logout <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 1024 1024"><path fill="currentColor" d="M868 732h-70.3c-4.8 0-9.3 2.1-12.3 5.8c-7 8.5-14.5 16.7-22.4 24.5a353.84 353.84 0 0 1-112.7 75.9A352.8 352.8 0 0 1 512.4 866c-47.9 0-94.3-9.4-137.9-27.8a353.84 353.84 0 0 1-112.7-75.9a353.28 353.28 0 0 1-76-112.5C167.3 606.2 158 559.9 158 512s9.4-94.2 27.8-137.8c17.8-42.1 43.4-80 76-112.5s70.5-58.1 112.7-75.9c43.6-18.4 90-27.8 137.9-27.8c47.9 0 94.3 9.3 137.9 27.8c42.2 17.8 80.1 43.4 112.7 75.9c7.9 7.9 15.3 16.1 22.4 24.5c3 3.7 7.6 5.8 12.3 5.8H868c6.3 0 10.2-7 6.7-12.3C798 160.5 663.8 81.6 511.3 82C271.7 82.6 79.6 277.1 82 516.4C84.4 751.9 276.2 942 512.4 942c152.1 0 285.7-78.8 362.3-197.7c3.4-5.3-.4-12.3-6.7-12.3m88.9-226.3L815 393.7c-5.3-4.2-13-.4-13 6.3v76H488c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h314v76c0 6.7 7.8 10.5 13 6.3l141.9-112a8 8 0 0 0 0-12.6"/></svg></button>
                    </form>
                </li>
                <!-- TODO: Update Links -->
            {/if}
        </ul>
    </div>
</div>

<label for="sidebar-drawer" class="btn btn-primary drawer-button absolute bottom-0 right-0 mb-6 mr-6 lg:hidden"
    ><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 1024 1024"><path fill="currentColor" d="M904 160H120c-4.4 0-8 3.6-8 8v64c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-64c0-4.4-3.6-8-8-8m0 624H120c-4.4 0-8 3.6-8 8v64c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-64c0-4.4-3.6-8-8-8m0-312H120c-4.4 0-8 3.6-8 8v64c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-64c0-4.4-3.6-8-8-8"/></svg></label>

<Toaster />

<style>
    form {
        display: inline;
    }
</style>

