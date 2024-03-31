import toast from 'svelte-french-toast';
import type { Renderable, ToastOptions } from 'svelte-french-toast';

export function normalToast(message: Renderable, opts: ToastOptions = {}) {
    const options = {
        style: 'background-color: oklch(var(--b1));color: oklch(var(--bc));',
        position: 'top-right',
    };
    return toast(message, Object.assign(options, opts));
}

export function errorToast(message: Renderable, opts: ToastOptions = {}) {
    const options = {
        style: 'background-color: oklch(var(--er));color: oklch(var(--erc));',
        position: 'top-right',
        iconTheme: {
            primary: 'oklch(var(--er))',
            secondary: 'oklch(var(--erc))',
        },
    };
    return toast.error(message, Object.assign(options, opts));
}

export function infoToast(message: Renderable, opts: ToastOptions = {}) {
    const options = {
        style: 'background-color: oklch(var(--in));color: oklch(var(--inc));',
        position: 'top-right',
    };
    return toast(message, Object.assign(options, opts));
}

export function successToast(message: Renderable, opts: ToastOptions = {}) {
    const options = {
        style: 'background-color: oklch(var(--su));color: oklch(var(--suc));',
        position: 'top-right',
        iconTheme: {
            primary: 'oklch(var(--su))',
            secondary: 'oklch(var(--suc))',
        },
    };
    return toast.success(message, Object.assign(options, opts));
}
