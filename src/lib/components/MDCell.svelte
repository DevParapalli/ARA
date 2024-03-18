<script lang="ts">
    import type { Plugin } from 'svelte-exmarkdown';
    import Markdown from 'svelte-exmarkdown';
    import typescript from 'highlight.js/lib/languages/typescript';
    import 'highlight.js/styles/github.css';
    import rehypeHighlight from 'rehype-highlight';

    let md = "```typescript\nconsole.log('Hello, world!');\n```";
    const plugins: Plugin[] = [
        {
            rehypePlugin: [rehypeHighlight, { ignoreMissing: true, languages: { typescript } }],
        },
    ];
</script>

<div class="w-full max-w-4xl">
    <textarea class="w-full" bind:value={md} />
    <Markdown {md} {plugins} />
</div>
