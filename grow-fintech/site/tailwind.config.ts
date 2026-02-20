import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "#080D1A",
        bg2: "#0D1525",
        bg3: "#111D33",
        accent: "#00E5B4",
        accent2: "#3B82F6",
        gray1: "#8B9AB5",
        gray2: "#4A5568",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Syne", "sans-serif"],
      },
      letterSpacing: {
        tightest: "-0.08em",
        tighter2: "-0.06em",
        tight2: "-0.04em",
      },
    },
  },
  plugins: [],
};
export default config;
