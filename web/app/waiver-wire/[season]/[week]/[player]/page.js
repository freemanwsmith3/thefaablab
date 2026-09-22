import Link from 'next/link';
import Image from 'next/image';
import { notFound } from 'next/navigation';
import { getPlayer, getWeek } from '../../../../../lib/api';
import { winningBucketIndex } from '../../../../../lib/derive';

export const revalidate = 300;

/**
 * Pre-render every player-week at build time. These pages are the long tail --
 * "john metchie faab bid" is the query this exists to answer -- so they should
 * be static HTML, not rendered on demand.
 */
export async function generateStaticParams() {
  const { getCurrentWeek } = await import('../../../../../lib/api');
  const { season, week } = await getCurrentWeek();
  const data = await getWeek(season, week);
  if (!data) return [];
  return data.players.map((p) => ({
    season: String(season),
    week: String(week),
    player: p.slug,
  }));
}

export async function generateMetadata({ params }) {
  const { season, week, player } = await params;
  const p = await getPlayer(season, week, player);
  if (!p) return { title: 'Player not found' };
  const median = p.hasData ? `Median bid ${p.median}% of budget.` : '';
  return {
    title: `${p.name} FAAB bid — Week ${week}`,
    description:
      `How much to bid on ${p.name} (${p.meta}) in Week ${week}. ${median} `
      + `Crowd bids plus what real Sleeper leagues actually paid.`,
    alternates: { canonical: `/waiver-wire/${season}/${week}/${player}` },
    openGraph: {
      title: `${p.name} FAAB bid — Week ${week}`,
      description: median || `Waiver wire bidding guidance for ${p.name}.`,
      images: p.image ? [{ url: p.image }] : undefined,
    },
  };
}

export default async function PlayerPage({ params }) {
  const { season, week, player } = await params;
  const p = await getPlayer(season, week, player);
  if (!p) notFound();

  const win = winningBucketIndex(p.buckets, p.mode);
  const winBucket = win >= 0 ? p.buckets[win] : null;

  // Structured data: tells search engines what the numbers on this page mean
  // rather than leaving them to infer it from markup.
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: `${p.name} FAAB bid guidance — Week ${week}, ${season}`,
    about: { '@type': 'Person', name: p.name },
    isPartOf: { '@type': 'WebSite', name: 'FAABLab' },
  };

  return (
    <main style={{ maxWidth: 760, margin: '0 auto', padding: '20px 14px 60px' }}>
      <script type="application/ld+json"
              dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <nav style={{ fontSize: 13, marginBottom: 14 }}>
        <Link href={`/waiver-wire/${season}/${week}`}>← Week {week} waiver wire</Link>
      </nav>

      <header style={{ display: 'flex', gap: 14, alignItems: 'center' }}>
        {p.image && (
          <Image src={p.image} alt={`${p.name} headshot`} width={88} height={88} priority
                 style={{ objectFit: 'contain', background: '#fff', borderRadius: 8 }} />
        )}
        <div>
          <h1 style={{ fontSize: 26, color: '#035e7b', margin: 0 }}>
            {p.name} FAAB bid — Week {week}
          </h1>
          <p style={{ margin: '2px 0 0', color: '#035e7b', fontWeight: 600 }}>{p.meta}</p>
        </div>
      </header>

      {!p.hasData ? (
        <p style={{ marginTop: 20, color: '#4d707c' }}>
          No bids on {p.name} yet this week. Be the first.
        </p>
      ) : (
        <section style={{ marginTop: 20 }}>
          <h2 style={{ fontSize: 18, color: '#035e7b' }}>What FAABLab bidders are paying</h2>
          <p style={{ color: '#14343f', lineHeight: 1.6 }}>
            Across <strong>{p.count.toLocaleString()}</strong> bids, the median bid on {p.name} is{' '}
            <strong>{p.median}% of budget</strong>
            {winBucket && (
              <> and the winning range is{' '}
                <strong>{winBucket.loPct}%–{winBucket.hiPct}%</strong></>
            )}.
          </p>

          <h3 style={{ fontSize: 15, color: '#035e7b' }}>Bid distribution</h3>
          <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: 14 }}>
            <thead>
              <tr><th align="left">Bid range</th><th align="left">Bids</th><th align="left">Share</th></tr>
            </thead>
            <tbody>
              {p.buckets.map((b, i) => (
                <tr key={i} style={{ borderTop: '1px solid #e3ecef' }}>
                  <td>{b.loPct}%–{b.hiPct}%</td>
                  <td>{b.bids}</td>
                  <td>{Math.round((b.bids / p.count) * 100)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {p.sleeper && (
        <section style={{ marginTop: 24 }}>
          <h2 style={{ fontSize: 18, color: '#035e7b' }}>What real Sleeper leagues paid</h2>
          <p style={{ lineHeight: 1.6 }}>
            Across <strong>{p.sleeper.leagues}</strong> Sleeper leagues that ran waivers,{' '}
            {p.name} went for an average of <strong>{p.sleeper.pct}% of budget</strong>
            {p.sleeper.bidToWin80 != null && (
              <>. A bid of <strong>{p.sleeper.bidToWin80}%</strong> would have won 80% of them</>
            )}.
          </p>
        </section>
      )}
    </main>
  );
}
