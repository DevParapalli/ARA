<script lang="ts">
    import { Carta, CartaEditor } from 'carta-md';
    import { attachment } from '@cartamd/plugin-attachment';
    import { emoji } from '@cartamd/plugin-emoji';
    import { slash } from '@cartamd/plugin-slash';
    import { code } from '@cartamd/plugin-code';
    import { math } from '@cartamd/plugin-math';
    // import 'carta-md/dark.css';
    import DOMPurify from 'isomorphic-dompurify';
    import { onMount } from 'svelte';
    import 'katex/dist/katex.css';
    const carta = new Carta({
        extensions: [
            attachment({
                async upload() {
                    return 'some-url-from-server.xyz';
                },
            }),
            emoji(),
            slash(),
            code({ autoDetect: 'true', lineNumbering: false }),
            math(),
        ],
        sanitizer: DOMPurify.sanitize,
    });
    let labels = {
        writeTab: 'Edit',
        previewTab: 'View',
    };
    export let value = '`This` is [an](url) **_~~example~~_** **inspired** by [GitHub](https://github.com)';

    onMount(() => {
        // carta.element?.querySelector('.carta-toolbar-left button:last-child')?.click();
        // Hack to make the editor cell, view first
    });
</script>

<CartaEditor bind:value mode="tabs" theme="ara" {labels} {carta} />
