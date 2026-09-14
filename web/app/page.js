import { redirect } from 'next/navigation';
import { getCurrentWeek } from '../lib/api';

// The root sends visitors to the live week rather than rendering a duplicate
// of it, so there is exactly one canonical URL per week.
export default async function Home() {
  const { season, week } = await getCurrentWeek();
  redirect(`/waiver-wire/${season}/${week}`);
}
