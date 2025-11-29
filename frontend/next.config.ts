import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: false, // Disabled for Leaflet compatibility
  images: {
    domains: ['localhost'],
  },
};

export default nextConfig;
