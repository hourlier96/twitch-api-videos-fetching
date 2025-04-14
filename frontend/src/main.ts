import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import type { ThemeDefinition } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'


// Icons
import '@mdi/font/css/materialdesignicons.css'
import { mdi } from 'vuetify/iconsets/mdi'

const customDarkTheme: ThemeDefinition = {
    dark: true,
    colors: {
      background: '#222831',
      surface: '#1c1e26',
      primary: '#6200EE',
      'primary-darken-1': '#3700B3',
      secondary: '#03DAC6',
      'secondary-darken-1': '#018786',
      error: '#B00020',
      info: '#2196F3',
      success: '#4CAF50',
      warning: '#FB8C00'
    }
  }

const vuetify = createVuetify({
    components,
    directives,
    theme: {
      defaultTheme: 'customDarkTheme',
      themes: {
        customDarkTheme
      }
    },
    icons: {
      sets: {
        mdi
      }
    },
  })
  

app.use(createPinia());
app.use(router);
app.use(vuetify)

app.mount("#app");
