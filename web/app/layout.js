import './globals.css';
import { Barlow } from 'next/font/google';

// next/font self-hosts the file and inlines the CSS, so there is no
// render-blocking request to Google and no layout shift from a late swap.
const barlow = Barlow({
  weight: ['400', '500', '600', '700'],
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-barlow',
});

const SITE = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.faablab.app';

export const metadata = {
  metadataBase: new URL(SITE),
  title: {
    default: 'FAABLab — crowd-sourced fantasy football FAAB bids',
    template: '%s | FAABLab',
  },
  description:
    'See what the crowd and real Sleeper leagues are paying for every waiver '
    + 'target, normalized to your league budget.',
  openGraph: { siteName: 'FAABLab', type: 'website' },
  robots: { index: true, follow: true },
};

export const viewport = {
  themeColor: '#035e7b',
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={barlow.variable}>
      <body>{children}</body>
    </html>
  );
}
