<script>
    import { Carta, CartaViewer } from 'carta-md';
    import { emoji } from '@cartamd/plugin-emoji';
    import { slash } from '@cartamd/plugin-slash';
    import { code } from '@cartamd/plugin-code';
    import { math } from '@cartamd/plugin-math';
    import 'carta-md/dark.css';
    import DOMPurify from 'isomorphic-dompurify';
    import 'katex/dist/katex.css';

    const carta = new Carta({
        extensions: [emoji(), slash(), code(), math()],
        // sanitizer: DOMPurify.sanitize
    });

    export let value = 'This is a **test** of the carta-md component.';
</script>

{#key value}
    <CartaViewer {carta} theme="github" bind:value />
{/key}
