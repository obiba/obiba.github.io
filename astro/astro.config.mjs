import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.obiba.org',
  integrations: [sitemap()],
  // Keep the old Jekyll URLs alive (external sites link to them).
  redirects: {
    '/pages/news/[...id]': '/news/[...id]',
    '/pages/products/[id]': '/products/[id]',
    '/pages/pkg': '/pkg',
    '/pages/rpm': '/rpm',
  },
});
