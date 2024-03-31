<script lang="ts">
    import { errorToast, infoToast, successToast } from '$lib/toast';
    import { onMount } from 'svelte';

    export let data;

    $: ({ supabase } = data);

    let currentTheme: string;

    onMount(() => {
        currentTheme = localStorage.getItem('theme') || '';
    });

    const themes = [
        // 'light',
        'dark',
        // 'cupcake',
        // 'bumblebee',
        // 'emerald',
        // 'corporate',
        'synthwave',
        // 'retro',
        // 'cyberpunk',
        // 'valentine',
        'halloween',
        // 'garden',
        'forest',
        'aqua',
        // 'lofi',
        // 'pastel',
        // 'fantasy',
        // 'wireframe',
        'black',
        'luxury',
        'dracula',
        // 'cmyk',
        // 'autumn',
        'business',
        // 'acid',
        // 'lemonade',
        'night',
        'coffee',
        // 'winter',
        'dim',
        // 'nord',
        'sunset',
    ];
</script>

<svelte:head>
    <title>User Profile | Project ARA</title>
</svelte:head>

<div class="flex h-full w-full items-center justify-center">
    <div class="mx-auto my-auto flex w-full max-w-7xl flex-col items-center gap-y-12 rounded-box bg-base-200 p-8">
        <h2 class="text-3xl">Settings</h2>
        <div class="data-container">
            <div class="flex w-full flex-row items-center gap-2">
                <div class="font-bold">Theme</div>
                <div class="contents">
                    <div
                        title="Change Theme"
                        class="dropdown dropdown-end ml-auto hidden [@supports(color:oklch(0%_0_0))]:block">
                        <div tabindex="0" role="button" class="btn btn-ghost">
                            <svg
                                width="20"
                                height="20"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                class="h-5 w-5 stroke-current md:hidden"
                                ><path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"
                                ></path
                                ></svg> <span class="hidden font-normal md:inline">Select Theme Here</span>
                            <svg
                                width="12px"
                                height="12px"
                                class="hidden h-2 w-2 fill-current opacity-60 sm:inline-block"
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 2048 2048"
                                ><path d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z"></path></svg>
                        </div>
                        <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                        <div
                            tabindex="0"
                            class="dropdown-content top-px mt-16 h-[28.6rem] max-h-[calc(100vh-10rem)] w-56 overflow-y-auto rounded-box border border-white/5 bg-base-200 text-base-content shadow-2xl outline outline-1 outline-black/5">
                            <div class="grid grid-cols-1 gap-3 p-3">
                                {#each themes as theme}
                                    <button
                                        class="text-start outline-offset-4 outline-base-content"
                                        data-set-theme={theme}
                                        data-act-class="[&amp;_svg]:visible"
                                        on:click={() => {
                                            document.documentElement.setAttribute('data-theme', theme);
                                            localStorage.setItem('theme', theme);
                                            currentTheme = theme;
                                            supabase.from('users').update({ theme }).eq('id', data.user.id).then(() => {
                                                successToast('Theme Updated');
                                            });
                                        }}
                                        ><span
                                            data-theme={theme}
                                            class="block w-full cursor-pointer rounded-btn bg-base-100 font-sans text-base-content"
                                            ><span class="grid grid-cols-5 grid-rows-3"
                                                ><span
                                                    class="col-span-5 row-span-3 row-start-1 flex items-center gap-2 px-4 py-3"
                                                    ><svg
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        width="16"
                                                        height="16"
                                                        viewBox="0 0 24 24"
                                                        fill="currentColor"
                                                        class="{currentTheme === theme ? 'visible':'invisible'} h-3 w-3 shrink-0"
                                                        ><path
                                                            d="M20.285 2l-11.285 11.567-5.286-5.011-3.714 3.716 9 8.728 15-15.285z"
                                                        ></path
                                                        ></svg> <span class="flex-grow text-sm">{theme}</span>
                                                    <span class="flex h-full shrink-0 flex-wrap gap-1"
                                                        ><span class="w-2 rounded-badge bg-primary"></span>
                                                        <span class="w-2 rounded-badge bg-secondary"></span>
                                                        <span class="w-2 rounded-badge bg-accent"></span>
                                                        <span class="w-2 rounded-badge bg-neutral"></span></span
                                                    ></span
                                                ></span
                                            ></span
                                        ></button>
                                {/each}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <h2 class="text-3xl">User Profile</h2>
        <!-- <pre>{JSON.stringify(data.user_data, null, 2)}</pre> -->
        <div class="data-container">
            <div class="data-row">
                <div class="data-heading">User ID</div>
                <button
                    on:click={() => {
                        navigator.clipboard.writeText(data.user.id);
                        infoToast('Copied to clipboard', { icon: '📋' });
                    }}
                    class="data"><span class="line-clamp-1">{data.user.id}</span></button>
            </div>
            <hr class="my-2 border-base-content/30" />
            <div class="data-row">
                <div class="data-heading">Email</div>
                <div class="data">{data.user.email}</div>
            </div>
            <hr class="my-2 border-base-content/30" />
            <div class="data-row">
                <div class="data-heading">Full Name</div>
                <input class="data-input input input-ghost" bind:value={data.user_data.full_name} />
            </div>
            <hr class="my-2 border-base-content/30" />
            <div class="data-row">
                <div class="data-heading">Nickname</div>
                <input class="data-input input input-ghost" bind:value={data.user_data.nickname} />
            </div>
            <hr class="my-2 border-base-content/30" />
            <div class="flex flex-col gap-2">
                <div class="font-bold">Custom Instructions</div>
                <div class="text-sm text-base-content/60">
                    Use this to store custom instructions for the text generation models.
                </div>
                <textarea
                    class="textarea textarea-bordered h-32 w-full p-2"
                    bind:value={data.user_data.custom_instructions}></textarea>
            </div>
            <hr class="my-4 border-base-content/30" />
            <div class="flex flex-col gap-2">
                <div class="font-bold">Custom Data</div>
                <div class="text-sm text-base-content/60">
                    Use this to store any extra data you want to associate with your account, such as keys, tokens, etc.
                </div>
                <textarea class="textarea textarea-bordered h-32 w-full p-2" bind:value={data.user_data.custom_data}
                ></textarea>
            </div>
            <hr class="my-4 border-base-content/30" />
            <div class="flex px-4">
                <button
                    on:click={async () => {
                        const { data: user_data, error } = await supabase
                            .from('users')
                            .update(data.user_data)
                            .eq('id', data.user.id);
                        if (error) {
                            // console.error(error);
                            errorToast('Update Failed');
                        } else {
                            successToast('Update Successful');
                        }
                    }}
                    class="btn btn-primary ml-auto">Update</button>
            </div>
        </div>
    </div>
</div>

<style lang="postcss">
    .data-container {
        @apply w-full max-w-2xl rounded-box bg-base-100 p-4 px-8;
    }

    .data-row {
        @apply line-clamp-1 flex h-12 w-full items-center justify-between gap-4;
    }

    .data-heading {
        @apply min-w-fit font-bold;
    }

    .data,
    .data > span {
        font-family: 'Fira Code', monospace;
        font-style: normal;
        @apply line-clamp-1;
    }

    .data-input {
        font-family: 'Fira Code', monospace;
        font-style: normal;
    }

    .textarea {
        font-family: 'Fira Code', monospace;
        font-style: normal;
    }
</style>
