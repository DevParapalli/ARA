<script lang="ts">

    let data: null | any = null;

    async function test_response() {
        const res = await fetch('http://localhost:4945')
        const _data = await res.json()
        data = _data
    }   

</script>

<h1>{(data) ? JSON.stringify(data):'Welcome to SvelteKit'}</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
<button class="p-4 bg-white text-black" on:click={test_response} ></button>