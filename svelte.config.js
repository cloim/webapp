import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import path from 'path';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess({
		postcss: true,
	}),
	kit: {
		adapter: adapter(),
		alias: {
			'$lib': path.resolve('./src/lib'),
			'$components': path.resolve('./src/lib/components'),
			'$images': path.resolve('./src/lib/images'),
		},
	},
};

export default config;
