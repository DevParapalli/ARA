<script lang="ts">
    // import MdCell from "$lib/components/MDCell.svelte";
    import CartaEditorCell from "$lib/components/CartaEditorCell.svelte";
    import CartaViewerCell from "$lib/components/CartaViewerCell.svelte";
	import { onMount } from "svelte";

    let value = "This is a **test** of the carta-md component.";
    onMount(() => {
        setTimeout(() => {
            value = "This is a **test** of the carta-md component. It's been updated!";
        }, 2000);
    })
</script>

<div class="flex flex-col w-full items-center justify-center py-2 px-6 gap-2">
    <!-- <MdCell /> -->
    <CartaEditorCell {value} />
    <div class="w-full max-w-3xl"><span class="mr-auto">Response: </span></div>
    <CartaViewerCell {value} />
</div>