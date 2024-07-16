/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}', './node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'],

	plugins: [require('flowbite/plugin')],

	darkMode: 'class',

	theme: {
		extend: {
			colors: {
				primary: {
					50: '#fafafa',
					100: '#f5f5f5',
					150: '#eeeeee',
					200: '#e5e5e5',
					300: '#d4d4d4',
					400: '#a3a3a3',
					500: '#737373',
					600: '#525252',
					700: '#404040',
					750: '#303030',
					800: '#262626',
					900: '#171717',
					950: '#0a0a0a'
				},
				accent: {
					100: '#0284c7',
					200: '#0369a1',
				}
			}
		}
	}
};
