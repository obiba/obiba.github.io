import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const news = (await getCollection('news')).sort((a, b) => +b.data.date - +a.data.date);
  return rss({
    title: 'OBiBa news',
    description: 'Releases and events of the OBiBa software suite',
    site: context.site,
    items: news.map((n) => ({
      title: n.data.title,
      pubDate: n.data.date,
      description: n.data.summary,
      link: `/news/${n.id}/`,
    })),
  });
}
