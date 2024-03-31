<script lang="ts">
    import CartaEditorCell from '$lib/components/CartaEditorCell.svelte';
    import CartaViewerCell from '$lib/components/CartaViewerCell.svelte';

    import { page } from '$app/stores';

    import { RemoteRunnable } from '@langchain/core/runnables/remote';
    import { AIMessageChunk } from '@langchain/core/messages';
    import { onMount } from 'svelte';
    import type { SupabaseClient } from '@supabase/supabase-js';
    import type { Database } from '$lib/supabaseTypes';

    //     let response: string = `
    // To create a scrollable div, you can use HTML and CSS to specify the overflow property for the div element. Here's an example of how you can do it:

    // HTML:
    // \`\`\`
    // <div class="scrollable-div">
    //   <!-- Content goes here -->
    // </div>
    // \`\`\`
    // CSS:
    // \`\`\`
    // .scrollable-div {
    //   height: 200px; /* set a fixed height for the div */
    //   overflow-y: scroll; /* enable vertical scrollbar */
    // }
    // \`\`\`
    // In this example, the div with the class "scrollable-div" will have a fixed height of 200px, and a vertical scrollbar will be displayed if the content inside the div exceeds the height of the div.

    // You can also make a div horizontally scrollable by using the CSS overflow property. Here are a few ways to do it:

    // 1. By setting the \`overflow-y\` to \`hidden\` and \`overflow-x\` to \`auto\`:
    // \`\`\`
    // .scrollable-div {
    //   overflow-y: hidden;
    //   overflow-x: auto;
    // }
    // \`\`\`
    // 2. By using the \`overflow\` property with the value of \`auto\`:
    // \`\`\`
    // .scrollable-div {
    //   overflow: auto;
    // }
    // \`\`\`
    // 3. By setting the \`overflow-y\` to \`hidden\` and \`overflow-x\` to \`auto\`:
    // \`\`\`
    // .scrollable-div {
    //   overflow-y: hidden;
    //   overflow-x: auto;
    // }
    // \`\`\`
    // For a horizontal scrollable bar, you can use the \`white-space\` property with the value of \`nowrap\` to wrap text in a single line. Here, the scroll div will be horizontally scrollable.

    // I hope this helps! Let me know if you have any questions.
    // `;

    let response = 'Use the input below to enter your query.';
    let metadata = {};
    let prompt: string = '';
    let status = '';
    let status_flag = '';
    let isloading = false;
    let context: string = '';
    let sources = [];

    onMount(() => {
        test_localhost_interval();
    });

    async function test_response() {
        isloading = true;
        try {
            const res = await fetch('http://localhost:4945');
            const _data = await res.json();
            response = JSON.stringify(_data);
        } catch (e) {
            alert('local server not running');
            console.error(e);
            isloading = false;
            return;
        }
        isloading = false;
    }

    async function test_localhost_interval() {
        isloading = true;
        // console.log($page.data.supabase)
        status = 'Connecting to localhost-server...';
        status_flag = 'text-warning';
        try {
            const res = await fetch('http://localhost:4945');
            // const _data = await res.json()
            // data = JSON.stringify(_data)
            isloading = false;
            status = 'Connected to localhost-server';
            status_flag = 'text-success';
            return true;
        } catch (e) {
            status = 'Failed to connect to localhost-server';
            status_flag = 'text-error';
            // setTimeout(test_localhost_interval, interval)
            // interval += 1000
            return false;
        }
    }

    async function test_langserve_rag() {
        isloading = true;
        try {
            const res = await fetch('http://localhost:4945');
        } catch (e) {
            alert('local server not running');
            console.debug(e);
            isloading = false;
            return;
        }

        if (!prompt) {
            prompt = 'Explain the technology behind Claude 3';
        }

        const remoteChain = new RemoteRunnable({ url: 'http://localhost:4945/rag' });
        // const result = await remoteChain.streamLog({prompt: prompt, context: "Machine Learning"})
        // response = ""
        // metadata = {}
        // sources = []
        // let state;
        // for await (const chunk of result) {
        //     let js_chunk = JSON.stringify(chunk)
        //     // console.log(state)
        //     // response += js_chunk + "\n\n"
        //     console.log(js_chunk)
        //     if (!state) {
        //         state = chunk
        //     }
        //     else {
        //         state = state.concat(chunk)
        //     }
        // }
        // response += JSON.stringify(state)
        // console.log(state);
        // // response = result.response
        // // metadata = result.metadata
        // // sources = result.sources
        // // data = result as string
        // console.log(response, metadata, sources)
        // isloading = false;

        const result = (await remoteChain.stream({ prompt: prompt, context: context })) as AsyncGenerator<
            AIMessageChunk | Object
        >;
        response = '';
        metadata = {};
        sources = [];
        let citations: any[] = [];
        try {
            for await (const chunk of result) {
                if (chunk instanceof AIMessageChunk) {
                    if ((chunk.content as string).startsWith('__citation__')) {
                        // console.debug('Citation:', chunk);
                        if (typeof chunk.content === 'string' && chunk.content.length > 13)
                            citations.push(JSON.parse(chunk.content.slice(13))[0]); // '__citation__:'
                    } else if ((chunk.content as string).startsWith('__search_queries__')) {
                        // console.debug('Search Query:', chunk);
                        // sources.push(chunk);
                        if (typeof chunk.content === 'string' && chunk.content.length > 19)
                            console.log(JSON.parse(chunk.content.slice(19))); // '__search_queries__:'
                    } else if ((chunk.content as string).startsWith('__search_results__')) {
                        // console.debug('Search Results:', chunk);
                        if (typeof chunk.content === 'string' && chunk.content.length > 19)
                            sources = JSON.parse(chunk.content.slice(19)).documents; // '__search_results__:'
                        // sources.push(chunk);
                    } else if ((chunk.content as string).startsWith('__stream_end__')) {
                        // console.debug('Stream end:', chunk);
                        if (typeof chunk.content === 'string' && chunk.content.length > 15)
                            Object.assign(metadata, JSON.parse(chunk.content.slice(15))); // '__stream_end__:'
                    } else {
                        response += chunk.content as string;
                    }
                } else {
                    console.debug(chunk);
                }
            }
        } catch (error) {
            console.error('Error during retrieval:', error);
        }
        // data = result as string
        const { data, error } = await $page.data.supabase
            .from('llm_runs')
            // .upsert({ id: metadata['run_id'], prompt: prompt, context: context, response: response, sources: sources });
            .upsert({
                id: `debug-run-${new Date().getTime()}`,
                prompt: prompt,
                context: context,
                response: response,
                sources: sources,
            });
        console.debug(response, metadata, sources, citations);
        // console.log(JSON.parse(result as string))
        isloading = false;
    }

    async function test_langserve_norag() {
        isloading = true;
        try {
            const res = await fetch('http://localhost:4945');
        } catch (e) {
            alert('local server not running');
            console.debug(e);
            isloading = false;
            return;
        }

        if (!prompt) {
            prompt = 'Explain Mixture of Experts.';
        }

        const remoteChain = new RemoteRunnable({ url: 'http://localhost:4945/norag' });
        const result = await remoteChain.stream({ prompt: prompt, context: context });
        response = '';
        metadata = {};
        sources = [];
        for await (const chunk of result) {
            if (typeof chunk === 'string') {
                response += chunk;
                continue;
            }
            if ('run_id' in (chunk as object) || 'prompt' in (chunk as object) || 'context' in (chunk as object)) {
                metadata = Object.assign(metadata, chunk);
            } else if ('sources' in (chunk as object)) {
                sources = chunk as Array<object>;
            } else if ('response' in (chunk as object)) {
                response += chunk['response'] as string;
            } else {
                // other.merge(chunk);
                console.debug(chunk);
            }
            // console.debug(chunk);
        }
        // data = result as string
        const { data, error } = await $page.data.supabase
            .from('llm_runs')
            .upsert({ id: metadata['run_id'], prompt: prompt, context: context, response: response, sources: sources });

        console.debug(response, metadata, sources, data, error);
        // console.log(JSON.parse(result as string))
        isloading = false;
    }
</script>

<div class="flex w-full flex-col items-center gap-4 p-10">
    <!-- <div class="mockup-code"><pre><code class="whitespace-pre-line">{(response) ? response:'Welcome to ARA-alpha'}</code></pre></div> -->
    <CartaViewerCell value={response} />
    <div class="flex w-full max-w-3xl justify-between"><span class="mr-auto text-sm {status_flag}">{status}</span></div>
    <!-- <div class="px-10 w-full"> 
        <div class="label">
            <label for="prompt" class="label-text">Prompt</label>
        </div>
        <input bind:value={prompt} id="prompt" name="prompt" type="text" class="input input-primary w-full">
    </div> -->
    <CartaEditorCell bind:value={prompt} />
    <hr />
    <CartaEditorCell bind:value={context} />
    <!-- <p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p> -->
    <button
        on:click={test_localhost_interval}
        class="{status_flag.includes('success') ? 'invisible' : 'visible'} btn btn-info btn-sm"
        >Retry Connection</button>
    <button disabled={isloading} on:click={test_langserve_rag} class="btn btn-primary">Test with RAG</button>
    <button disabled={isloading} on:click={test_langserve_norag} class="btn btn-secondary">Test without RAG</button>
    <div class="flex w-full items-center justify-center">
        <span id="loader" class="loading loading-infinity w-[5rem] {isloading ? 'visible' : 'invisible'}"></span>
    </div>
    <div class="w-full max-w-3xl">
        <span class="ml-auto text-sm">{'run_id' in metadata ? JSON.stringify(metadata) : ''}</span>
    </div>
</div>

<style>
    @keyframes hue-rotate-animate {
        0% {
            filter: hue-rotate(0deg);
        }
        100% {
            filter: hue-rotate(360deg);
        }
    }

    #loader {
        color: #ff0000;
        animation: hue-rotate-animate 30s infinite linear;
    }
</style>
