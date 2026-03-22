/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brass: '#c4a35a',
        surface: {
          0: '#0a0908',
          1: '#12110f',
          2: '#1a1816',
          3: '#221f1c',
          4: '#2a2722',
        },
        status: {
          stable: '#4ade80',
          elevated: '#fbbf24',
          high: '#f97316',
          critical: '#ef4444',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
        display: ['Josefin Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
