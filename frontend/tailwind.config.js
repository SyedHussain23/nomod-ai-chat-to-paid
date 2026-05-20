/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0B0D12",
        panel: "#11141B",
        card: "#161A23",
        border: "#222734",
        ink: {
          DEFAULT: "#E7EAF0",
          dim: "#8B91A1",
          faint: "#5B6172",
        },
        brand: {
          DEFAULT: "#7C5CFF",
          soft: "#A493FF",
          glow: "#5B3CFF",
        },
        good: "#22C55E",
        warn: "#F59E0B",
        bad: "#EF4444",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "ui-sans-serif", "Segoe UI", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 0 0 rgba(255,255,255,0.04) inset, 0 8px 24px -12px rgba(0,0,0,0.6)",
      },
    },
  },
  plugins: [],
};
