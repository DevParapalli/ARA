<script>
	import '../app.pcss';
	import { enhance } from '$app/forms';
    import { invalidate, invalidateAll, goto } from '$app/navigation';
    import { onMount } from 'svelte';

    export let data;

    $: ({ supabase } = data);

    onMount(async () => {
        supabase.auth.onAuthStateChange((event, _session) => {
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
        return () => subscription.unsubscribe();
    });

    const submitLogout = async ({ cancel }) => {
        const { error } = await data.supabase.auth.signOut();
        if (error) {
            console.log(error);
        }
        cancel();
        await goto('/');
    };
</script>


<div class="drawer lg:drawer-open">
    <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex flex-col items-center justify-center w-full h-full">
        <slot />
      <label for="my-drawer-2" class="btn btn-primary drawer-button lg:hidden absolute bottom-0 right-0 mr-4 mb-4">MENU</label>
    
    </div> 
    <div class="drawer-side">
      <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label> 
      <ul class="menu p-4 w-80 min-h-full bg-base-200 text-base-content">
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
        
        {/if}
      </ul>
    
    </div>
  </div>

<style>
    form {
        display: inline;
    }
</style>