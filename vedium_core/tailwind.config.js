/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./vedium_core/**/*.{html,js,py}",
        "./vedium_core/templates/**/*.html",
        "./vedium_core/www/**/*.html",
        "./vedium_core/public/**/*.{js,html}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Kanit', 'sans-serif'],
            },
            colors: {
                primary: '#FECF03', // Yellow
                action: '#FF2712',  // Red
                footer: '#2A3290',  // Blue
                'hero-text': '#FEA69F', // Pinkish text
                'light-bg': '#FFF9F9', // Very light pink/white
                'brand-white': '#FFFFFF',
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'hero-overlay': 'linear-gradient(to right, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0) 100%)',
            },
        },
    },
    plugins: [],
}
