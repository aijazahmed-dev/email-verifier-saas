/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',      // All templates in the main folder
    './**/templates/**/*.html',   // Templates inside Django apps
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Rubik', 'sans-serif'], // Set Rubik as the default sans-serif font
      },
      colors: {
        primary: '#1D4ED8',    // Example primary color (blue)
        secondary: '#F59E0B',  // Example secondary color (yellow/orange)
      },
      maxWidth: {
        'container': '1100px', // Example max width for container
      },
    },
  },
  plugins: [],
}
