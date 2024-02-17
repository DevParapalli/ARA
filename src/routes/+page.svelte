<script lang="ts">

    import {RemoteRunnable} from '@langchain/core/runnables/remote'

    let data: string = "";

    async function test_response() {
        try {
            const res = await fetch('http://localhost:4945')
            const _data = await res.json()
            data = JSON.stringify(_data) 
        }
        catch (e) {
            alert('local server not running')
            console.log(e)
            return;
        }
        
    }
    
    async function test_langserve_chat() {
        try {
            const res = await fetch('http://localhost:4945')
        }
        catch (e) {
            alert('local server not running')
            console.log(e)
            return;
        }
        const remoteChain = new RemoteRunnable({url: 'http://localhost:4945/chat'})
        const result = await remoteChain.invoke('Hi there!')
        // for await (const chunk of result) {
        //     data += chunk
        // }
        data = result as string
    }

    async function test_langserve_code() {
        try {
            const res = await fetch('http://localhost:4945')
        }
        catch (e) {
            alert('local server not running')
            console.log(e)
            return;
        }
        const remoteChain = new RemoteRunnable({url: 'http://localhost:4945/code'})
        const result = await remoteChain.invoke('Python code for factorial')
        data = JSON.parse(result as string)[0]['code'] as string
        // console.log(JSON.parse(result as string))
    
    }

</script>

<div class="mockup-code">
    <pre><code class="whitespace-pre-line">{(data) ? data:'Welcome to SvelteKit'}</code></pre>
</div>
<!-- <p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p> -->
<button on:click={test_response} class="p-4 bg-red-500 text-white/60" >Test localhost</button>
<button on:click={test_langserve_chat} class="p-4 bg-blue-500 text-white/60">Test LangServe Chat</button>
<button on:click={test_langserve_code} class="p-4 bg-green-500 text-white/60">Test LangServe Code</button>