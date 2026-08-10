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
                // Vedium Brand Colors
                primary: {
                    DEFAULT: '#166534',
                    50: '#f0fdf4',
                    100: '#dcfce7',
                    200: '#bbf7d0',
                    300: '#86efac',
                    400: '#4ade80',
                    500: '#22c55e',
                    600: '#16a34a',
                    700: '#15803d',
                    800: '#166534',
                    900: '#14532d',
                },
                secondary: {
                    DEFAULT: '#ca8a04',
                    700: '#a16207',
                },
                accent: '#6f5850',
                // Dark Theme
                'dark-bg': '#0f1419',
                'dark-surface': '#1a1f26',
                'dark-border': '#374151',
                'dark-text': '#f3f4f6',
                'dark-muted': '#9ca3af',
                // Legacy support
                action: '#FF2712',
                footer: '#2A3290',
                'hero-text': '#FEA69F',
                'light-bg': '#FFF9F9',
                'brand-white': '#FFFFFF',
            },
            boxShadow: {
                'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
                'glow': '0 0 20px rgba(22, 101, 52, 0.3)',
                'glow-gold': '0 0 20px rgba(202, 138, 4, 0.3)',
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'hero-overlay': 'linear-gradient(to right, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0) 100%)',
            },
        },
    },
    darkMode: 'class',
    plugins: [],
}
