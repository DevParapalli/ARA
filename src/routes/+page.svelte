<script lang="ts">

    import {RemoteRunnable} from '@langchain/core/runnables/remote'
	import { onMount } from 'svelte';

    let data: string = "";
    let metadata = {};
    let prompt: string = "";
    let status = "";
    let status_flag = '';
    let isloading = false;
    let interval = 1000;

    onMount(() => {
        test_localhost_interval()
    })

    async function test_response() {
        isloading = true;
        try {
            const res = await fetch('http://localhost:4945')
            const _data = await res.json()
            data = JSON.stringify(_data) 
        }
        catch (e) {
            alert('local server not running')
            console.log(e)
            isloading = false;
            return;
        }
        isloading = false;
    }
    
    async function test_localhost_interval() {
        isloading = true;
        status = "Connecting to localhost-server..."
        status_flag = "text-warning"
        try {
            const res = await fetch('http://localhost:4945')
            // const _data = await res.json()
            // data = JSON.stringify(_data) 
            isloading = false;
            status = "Connected to localhost-server"
            status_flag = "text-success"
            return true;
        }
        catch (e) {
            status = 'Failed to connect to localhost-server'
            status_flag = "text-error"
            // setTimeout(test_localhost_interval, interval)
            // interval += 1000
            return false;
        }
    }

    async function test_langserve_chat() {
        isloading = true;
        try {
            const res = await fetch('http://localhost:4945')
        }
        catch (e) {
            alert('local server not running')
            console.log(e)
            isloading = false;
            return;
        }
        const remoteChain = new RemoteRunnable({url: 'http://localhost:4945/chat'})
        const result = await remoteChain.stream(prompt)
        data = ""
        for await (const chunk of result) {
            if (typeof chunk === 'string')
                data += chunk
            else {
                metadata = chunk as object
            }
        }
        // data = result as string
        isloading = false;
    }

    async function test_langserve_code() {
        isloading = true;
        try {
            const res = await fetch('http://localhost:4945')
        }
        catch (e) {
            alert('local server not running')
            console.log(e)
            isloading = false;
            return;
        }
        const remoteChain = new RemoteRunnable({url: 'http://localhost:4945/code'})
        const result = await remoteChain.invoke(prompt)
        data = JSON.parse(result as string)[0]['code'] as string
        // console.log(JSON.parse(result as string))
        isloading = false;
    }

</script>

<div class="flex p-10 flex-col space-y-4">
    <div class="mockup-code">
        <pre><code class="whitespace-pre-line">{(data) ? data:'Welcome to ARA-alpha'}</code></pre>
    </div>
    <div class="flex w-full justify-between"><span class="text-sm {status_flag}">{status}</span><span class="text-sm">{('run_id' in metadata) ? JSON.stringify(metadata): ""}</span></div>
    <div class="px-10 w-full"> 
        <div class="label">
            <label for="prompt" class="label-text">Prompt</label>
        </div>
        <input bind:value={prompt} id="prompt" name="prompt" type="text" class="input input-primary w-full">
    </div>
    <!-- <p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p> -->
    <button on:click={test_localhost_interval} class="{(status_flag.includes('success')) ? 'invisible':'visible'} btn btn-sm btn-info" >Retry Connection</button>
    <button disabled={isloading} on:click={test_langserve_chat} class="btn btn-primary">Test LangServe Chat</button>
    <button disabled={isloading} on:click={test_langserve_code} class="btn btn-secondary">Test LangServe Code</button>
    <div class="flex w-full items-center justify-center"><span id="loader" class="loading loading-infinity w-[5rem] {isloading ? 'visible':'invisible'}"></span></div>
    
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