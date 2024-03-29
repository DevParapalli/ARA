// import { setHeaders } from '@sveltejs/kit';

export async function GET({ fetch, url, setHeaders }) {
    const _favicon = url.searchParams.get('url');
    const hostname = new URL(_favicon).hostname;
    const res = await fetch(`https://www.google.com/s2/favicons?domain=${hostname}&sz=32`);

    setHeaders({
        'Content-Type': 'image/png',
        'Cache-Control': 'public, max-age=604800, immutable',
    });

    return new Response(res.body);
}
