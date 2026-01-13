/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./vedium_core/**/*.{html,js,py}",
        "./vedium_core/templates/**/*.html",
        "./vedium_core/public/**/*.{js,html}",
    ],
    darkMode: 'class',
    theme: {
        extend: {
            // ===========================================
            // PALETA "RAÍZES DE LUXO" - Vedium Design
            // ===========================================
            colors: {
                // Primary - Deep Forest Green (Confiança / Crescimento)
                primary: {
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
                    950: '#052e16',
                    DEFAULT: '#166534', // forest-800
                },

                // Secondary - Warm Gold (Premium / Valor)
                secondary: {
                    50: '#fefce8',
                    100: '#fef9c3',
                    200: '#fef08a',
                    300: '#fde047',
                    400: '#facc15',
                    500: '#eab308',
                    600: '#ca8a04',
                    700: '#a16207',
                    800: '#854d0e',
                    900: '#713f12',
                    950: '#422006',
                    DEFAULT: '#ca8a04', // gold-600
                },

                // Accent - Deep Earth Brown (Solidez / Raízes)
                accent: {
                    50: '#fdf8f6',
                    100: '#f2e8e5',
                    200: '#eaddd7',
                    300: '#e0cec7',
                    400: '#d2bab0',
                    500: '#bfa094',
                    600: '#a18072',
                    700: '#8b6f65',
                    800: '#6f5850',
                    900: '#5a483f',
                    950: '#3d312a',
                    DEFAULT: '#6f5850', // earth-800
                },

                // Neutral - Sophisticated Grays
                neutral: {
                    50: '#fafafa',
                    100: '#f5f5f5',
                    200: '#e5e5e5',
                    300: '#d4d4d4',
                    400: '#a3a3a3',
                    500: '#737373',
                    600: '#525252',
                    700: '#404040',
                    800: '#262626',
                    900: '#171717',
                    950: '#0a0a0a',
                },

                // Background Dark Theme
                dark: {
                    bg: '#0f1419',
                    surface: '#1a1f26',
                    border: '#2f3640',
                    text: '#e7e9ea',
                    muted: '#8b98a5',
                },

                // Status Colors
                success: '#22c55e',
                warning: '#f59e0b',
                error: '#ef4444',
                info: '#3b82f6',
            },

            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                display: ['Outfit', 'Inter', 'sans-serif'],
                mono: ['JetBrains Mono', 'monospace'],
            },

            fontSize: {
                '2xs': ['0.625rem', { lineHeight: '0.75rem' }],
            },

            borderRadius: {
                '4xl': '2rem',
                '5xl': '2.5rem',
            },

            boxShadow: {
                'glow': '0 0 20px rgba(22, 101, 52, 0.3)',
                'glow-gold': '0 0 20px rgba(202, 138, 4, 0.3)',
                'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
            },

            animation: {
                'fade-in': 'fadeIn 0.5s ease-out',
                'slide-up': 'slideUp 0.5s ease-out',
                'pulse-slow': 'pulse 3s infinite',
            },

            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideUp: {
                    '0%': { opacity: '0', transform: 'translateY(20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },

            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'gradient-vedium': 'linear-gradient(135deg, #166534 0%, #052e16 100%)',
                'gradient-gold': 'linear-gradient(135deg, #ca8a04 0%, #854d0e 100%)',
            },
        },
    },
    plugins: [],
}
