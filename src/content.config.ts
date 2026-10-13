import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Keep ids as the file path (e.g. "release/agate/5.0"); the default slugifier drops the dot.
const pathId = ({ entry }: { entry: string }) => entry.replace(/\.md$/, '');

const news = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/news', generateId: pathId }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    product: z.string().optional(),
    summary: z.string().optional(),
  }),
});

const products = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/products' }),
  schema: z.object({
    name: z.string(),
    title: z.string(),
    tagline: z.string(),
    order: z.number(),
    icon: z.string().optional(),
    docs: z.string().url().optional(),
    github: z.string().url().optional(),
    demo: z.string().url().optional(),
  }),
});

export const collections = { news, products };
