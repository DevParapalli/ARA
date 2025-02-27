import daisyui from 'daisyui';
import typography from '@tailwindcss/typography';
import forms from '@tailwindcss/forms';

/** @type {import('tailwindcss').Config}*/
const config = {
    content: ['./src/**/*.{html,js,svelte,ts}'],

    theme: {
        extend: {},
    },

    plugins: [forms, typography, daisyui],

    daisyui: {
        themes: [
            'light',
            'dark',
            'cupcake',
            // 'bumblebee',
            'emerald',
            'corporate',
            'synthwave',
            // 'retro',
            // 'cyberpunk',
            // 'valentine',
            'halloween',
            'garden',
            'forest',
            'aqua',
            // 'lofi',
            // 'pastel',
            'fantasy',
            // 'wireframe',
            // 'black',
            // 'luxury',
            'dracula',
            'cmyk',
            'autumn',
            'business',
            // 'acid',
            // 'lemonade',
            'night',
            'coffee',
            'winter',
            'dim',
            'nord',
            'sunset',
        ],
    },
};

module.exports = config;
