import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Grow Fintech | Fintech Marketing Agency | Paid Media, GEO & Growth Strategy",
  description:
    "Grow Fintech is a specialist marketing agency for fintech companies. Paid acquisition, GEO (Generative Engine Optimization), demand generation, and fractional CMO. built around revenue, not reports.",
  keywords: [
    "fintech marketing agency",
    "marketing agency for fintech",
    "fintech growth marketing",
    "fintech paid media agency",
    "fintech SEO agency",
    "GEO generative engine optimization fintech",
  ],
  openGraph: {
    title: "Grow Fintech | Fintech Marketing Agency",
    description: "We grow fintechs. Profitably. Paid acquisition, GEO, demand generation, and fractional CMO built around revenue. not reports.",
    url: "https://grow-fintech.io",
    siteName: "Grow Fintech",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Grow Fintech | Fintech Marketing Agency",
    description: "We grow fintechs. Profitably.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
