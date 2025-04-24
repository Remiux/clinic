/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./**/templates/**/*.html","./node_modules/flyonui/dist/js/*.js","./node_modules/notyf/**/*.js","./node_modules/datatables.net/js/dataTables.min.js"],
  plugins: [
    require("flyonui"),
    require("flyonui/plugin"),
    require("tailwindcss-motion"), // Require only if you want to use FlyonUI JS component
  ],
  darkMode: "media",
  lightMode: "media",
  theme: {
    extend: {
      fontFamily: {

      },
      'animation': {
            'text':'text 5s ease infinite',
        },
        'keyframes': {
            'text': {
                '0%, 100%': {
                   'background-size':'200% 200%',
                    'background-position': 'left center'
                },
                '50%': {
                   'background-size':'200% 200%',
                    'background-position': 'right center'
                }
            },
        }
    },
  },
  flyonui: {
    themes: ['light', 'dark'],
    vendors: true
  },
  darkMode: ['class', '[data-theme="dark"]'],
  
  
}

