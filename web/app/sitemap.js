import { getCurrentWeek, getWeek } from '../lib/api';

const SITE = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.faablab.app';

/**
 * Every week and every player-week, so crawlers can find the long-tail pages
 * without depending on internal linking alone.
 */
export default async function sitemap() {
  const { season, week } = await getCurrentWeek();
  const entries = [{ url: SITE, changeFrequency: 'daily', priority: 1 }];

  for (let w = 1; w <= week; w += 1) {
    entries.push({
      url: `${SITE}/waiver-wire/${season}/${w}`,
      changeFrequency: w === week ? 'hourly' : 'monthly',
      priority: w === week ? 0.9 : 0.5,
    });
  }

  const data = await getWeek(season, week);
  for (const p of data?.players || []) {
    entries.push({
      url: `${SITE}/waiver-wire/${season}/${week}/${p.slug}`,
      changeFrequency: 'daily',
      priority: 0.7,
    });
  }
  return entries;
}
