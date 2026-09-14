/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    // Headshots come from Sleeper's public CDN.
    remotePatterns: [{ protocol: 'https', hostname: 'sleepercdn.com' }],
  },
};
export default nextConfig;
