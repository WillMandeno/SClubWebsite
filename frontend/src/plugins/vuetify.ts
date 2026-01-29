import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

const SJCLightColourScheme = {
  dark: false,
  colors: {
    background: '#F6F8FA',
    surface: '#f1f1f1ff',
    primary: '#03772f',
    secondary: '#ffaa00ff',
    pending: '#ffc24966',
    error: '#d20000ff',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FB8C00',
  },
}

export default createVuetify({
  icons: { defaultSet: 'mdi', aliases, sets: { mdi } },
  theme: {
    defaultTheme: 'SJCLightColourScheme',
    themes: {
      SJCLightColourScheme,
    },
  },
  defaults: {
    VBtn: { rounded: true, elevation: 0 },
    VToolbarTitle: {
      style: 'font-family: \"Bungee\", Rubik, Inter, sans-serif; text-transform: none; letter-spacing: 0;',
    },
    VCardTitle: {
      style: 'font-family: \"Bungee\", Rubik, Inter, sans-serif; text-transform: none; letter-spacing: 0;',
    },
    VCard: { elevation: 1 },
    VAppBar: { elevation: 2 },
  },
})