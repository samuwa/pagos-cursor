/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f8ff',
          100: '#e0f2fe',
          500: '#0073ea',
          600: '#0056b3',
          700: '#004085',
        },
        secondary: {
          50: '#f0fdf4',
          100: '#dcfce7',
          500: '#00c875',
          600: '#00a05e',
          700: '#007847',
        },
        warning: {
          50: '#fffbeb',
          100: '#fef3c7',
          500: '#ffcb00',
          600: '#d97706',
          700: '#b45309',
        },
        danger: {
          50: '#fef2f2',
          100: '#fee2e2',
          500: '#e2445c',
          600: '#dc2626',
          700: '#b91c1c',
        },
        neutral: {
          50: '#f5f6f8',
          100: '#e5e7eb',
          200: '#d0d4dc',
          300: '#9ca3af',
          400: '#6b7280',
          500: '#4b5563',
          600: '#374151',
          700: '#323338',
          800: '#1f2937',
          900: '#111827',
        }
      },
      fontFamily: {
        sans: ['"Open Sans"', '"Inter"', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'xs': ['12px', { lineHeight: '1.6' }],
        'sm': ['14px', { lineHeight: '1.6' }],
        'base': ['14px', { lineHeight: '1.6' }],
        'lg': ['16px', { lineHeight: '1.6' }],
        'xl': ['18px', { lineHeight: '1.6' }],
        '2xl': ['20px', { lineHeight: '1.6' }],
        '3xl': ['24px', { lineHeight: '1.6' }],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      borderRadius: {
        'md': '6px',
      },
      boxShadow: {
        'soft': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'medium': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      }
    },
  },
  plugins: [],
} 