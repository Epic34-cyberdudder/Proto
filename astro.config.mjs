// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'Discord AI Bot', // Change 'My Docs' to your desired title here!
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/Epic34-cyberdudder/Discord-AI-BOT' }],
			sidebar: [
				{
					label: 'Guides',
					items: [
						{ label: 'Installation Guide', slug: 'guides/installation' },
						{ label: 'Configuration Guide', slug: 'guides/configuration' },
					],
				},
				{
					label: 'Reference',
					items: [{ autogenerate: { directory: 'reference' } }],
				},
			],
		}),
	],
});