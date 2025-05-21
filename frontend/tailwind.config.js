/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./App.{js,jsx,ts,tsx}", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#4F46E5", // Indigo-600
          light: "#818CF8", // Indigo-400
          dark: "#3730A3", // Indigo-800
        },
        secondary: {
          DEFAULT: "#10B981", // Emerald-500
          light: "#34D399", // Emerald-400
          dark: "#059669", // Emerald-600
        },
        background: {
          DEFAULT: "#F9FAFB", // Gray-50
          dark: "#F3F4F6", // Gray-100
        },
      },
      fontFamily: {
        sans: ["System", "sans-serif"],
      },
    },
  },
  plugins: [],
};
