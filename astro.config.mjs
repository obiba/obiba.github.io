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
    '/pages/infra': '/infra',
    '/pages/stories': '/stories',
    '/pages/news': '/news',
    '/pages/download': '/download',
    '/pages/support': '/support',
    '/pages/about': '/about',
    '/pages/license': '/about/#license',
    '/pages/presentations': '/presentations',
    '/pages/publications': '/publications',
    '/pages/jobs': '/about',
    '/pages/jobs/java': '/about',
    '/pages/documentation': '/#products',
    '/pages/plugins': 'https://plugins.obiba.org/',
    '/pages/integrated-suite': '/integrated-suite',
    '/node/62': '/about/#license',
    // Legacy products, not ported.
    '/pages/products/mica1': '/products/mica',
    '/pages/products/onyx': 'https://github.com/obiba/onyx',
  },
});
