// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://epic34-cyberdudder.github.io',
  base: '/Proto',

  integrations: [
    starlight({
      title: 'Proto',

      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/Epic34-cyberdudder/Discord-AI-BOT',
        },
      ],

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