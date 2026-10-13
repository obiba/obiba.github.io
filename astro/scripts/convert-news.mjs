// One-off: convert the Jekyll news (_data/news.yml + stub page + HTML partial) into
// Markdown files of the `news` content collection. Bodies stay HTML (valid in .md);
// new posts should be written in plain Markdown.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { parse } from 'yaml';

const jekyll = new URL('../../', import.meta.url).pathname;
const out = new URL('../src/content/news/', import.meta.url).pathname;

const { data } = parse(readFileSync(join(jekyll, '_data/news.yml'), 'utf8'));
let written = 0;
const missing = [];

for (const item of data) {
  const id = item.url.replace(/^\/|\/$/g, '');
  const stub = join(jekyll, 'pages/news', id, 'index.html');
  if (!existsSync(stub)) { missing.push(id); continue; }

  const body = readFileSync(stub, 'utf8').match(/sectionBody="([^"]+)"/)?.[1];
  const html = readFileSync(join(jekyll, '_includes', body), 'utf8')
    .replace(/<i class="fa [^"]*"><\/i>\s*/g, '') // font-awesome icons
    .replace(/ class="obiba-[^"]*"/g, '') // old theme classes
    .replace(/\/assets\/themes\/bootstrap\/img\//g, '/img/') // images live in public/img
    .replace(/href="\/pages\/(pkg|rpm|infra|stories)\/?"/g, 'href="/$1/"') // ported pages
    .replace(/<p>\s*(<ul>[\s\S]*?<\/ul>)\s*<\/p>/g, '$1') // invalid <p><ul>
    .trim();

  const [kind, product] = id.split('/');
  const fm = {
    title: item.title,
    date: item.date instanceof Date ? item.date.toISOString().slice(0, 10) : String(item.date),
    ...(kind === 'release' && { product: product === 'mica2' ? 'mica' : product }),
    ...(item.summary && { summary: item.summary }),
  };
  const yaml = Object.entries(fm).map(([k, v]) => `${k}: ${JSON.stringify(v)}`).join('\n');

  const file = join(out, `${id}.md`);
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, `---\n${yaml}\n---\n\n${html}\n`);
  written++;
}

console.log(`wrote ${written} news items`);
if (missing.length) console.log(`no stub page for: ${missing.join(', ')}`);
