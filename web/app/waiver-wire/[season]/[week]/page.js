import Link from 'next/link';
import Image from 'next/image';
import { notFound } from 'next/navigation';
import { getWeek } from '../../../../lib/api';

export const revalidate = 300;

export async function generateMetadata({ params }) {
  const { season, week } = await params;
  const data = await getWeek(season, week);
  if (!data) return { title: `Week ${week} waiver wire` };
  const names = data.players.slice(0, 5).map((p) => p.name).join(', ');
  return {
    title: `Week ${week} FAAB waiver wire bids (${season})`,
    description:
      `What to bid on Week ${week} waiver targets: ${names}. Crowd-sourced FAAB `
      + `bids plus real Sleeper league results, shown in your league's dollars.`,
    alternates: { canonical: `/waiver-wire/${season}/${week}` },
    openGraph: {
      title: `Week ${week} FAAB waiver wire bids`,
      description: `Median bids and winning ranges for ${data.players.length} waiver targets.`,
    },
  };
}

export default async function WeekPage({ params }) {
  const { season, week } = await params;
  const data = await getWeek(season, week);
  if (!data || !data.players.length) notFound();

  return (
    <main style={{ maxWidth: 1180, margin: '0 auto', padding: '20px 14px 60px' }}>
      <h1 style={{ fontSize: 26, color: '#035e7b', margin: '0 0 6px' }}>
        Week {data.week} FAAB waiver wire bids
      </h1>
      <p style={{ color: '#4d707c', maxWidth: '46ch', margin: '0 0 20px' }}>
        What the crowd and real Sleeper leagues are paying for each {season} Week{' '}
        {data.week} waiver target. Bids are percent of budget, so they compare across leagues.
      </p>

      {/* Server-rendered list: this is the content a crawler indexes. */}
      <ul style={{ listStyle: 'none', padding: 0, display: 'grid', gap: 12,
                   gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
        {data.players.map((p) => (
          <li key={p.id} style={{ background: '#fff', border: '2px solid #035e7b',
                                  borderRadius: 8, padding: 14 }}>
            <article>
              <Link href={`/waiver-wire/${season}/${week}/${p.slug}`}
                    style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                {p.image && (
                  <Image src={p.image} alt={`${p.name} headshot`} width={56} height={56}
                         style={{ objectFit: 'contain', background: '#fff', borderRadius: 6 }} />
                )}
                <span>
                  <h2 style={{ fontSize: 18, color: '#035e7b', margin: 0 }}>{p.name}</h2>
                  <span style={{ fontSize: 14, color: '#035e7b', fontWeight: 600 }}>{p.meta}</span>
                </span>
              </Link>
              {p.hasData && (
                <p style={{ margin: '10px 0 0', fontSize: 14, color: '#4d707c' }}>
                  Median bid <strong>{p.median}%</strong> of budget from{' '}
                  <strong>{p.count.toLocaleString()}</strong> bids
                  {p.sleeper && (
                    <> · Sleeper leagues paid <strong>{p.sleeper.pct}%</strong> across{' '}
                      {p.sleeper.leagues} leagues</>
                  )}
                </p>
              )}
            </article>
          </li>
        ))}
      </ul>
    </main>
  );
}
