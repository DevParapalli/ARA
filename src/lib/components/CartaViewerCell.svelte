<script>
    import { Carta, CartaViewer } from 'carta-md';
    import { emoji } from '@cartamd/plugin-emoji';
    import { slash } from '@cartamd/plugin-slash';
    import { code } from '@cartamd/plugin-code';
    import { math } from '@cartamd/plugin-math';
    // import 'carta-md/dark.css';
    import DOMPurify from 'isomorphic-dompurify';
    import 'katex/dist/katex.css';

    const carta = new Carta({
        extensions: [emoji(), slash(), code(), math()],
        // sanitizer: DOMPurify.sanitize
    });

    export let value = `
Use this to test the theme switcher, make sure you can read the text clearly and without strain.
\`\`\`js

function changeTheme() {
    const btn = document.getElementsByTagName('button')[0]
    let html = document.getElementsByTagName('html')[0];
    if (html.getAttribute('data-theme') == 'dark') {
        html.setAttribute('data-theme', 'light');
        setTimeout(() => { btn.innerHTML = MOON }, duration)
    }
    else {
        html.setAttribute('data-theme', 'dark');
        setTimeout(() => { btn.innerHTML = SUN }, duration)
    }
}
\`\`\`
`;
</script>

{#key value}
    <CartaViewer {carta} theme="ara" bind:value />
{/key}
