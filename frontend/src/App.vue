<template>
  <v-app>
    <v-app-bar color="primary" dark>
      <v-toolbar-title class="d-flex align-center">
        <v-icon class="mr-3 mb-1" @click="router.push('/')">
          <v-img :src="EagleLogoGreenBackground" alt="SClub Logo" contain />
        </v-icon>
        <span class="toolbar-title-text" @click="router.push('/')">SClub Calendar</span>
      </v-toolbar-title>
      <v-btn class="mx-2" v-if="isAuthenticated" text @click="logout">Logout</v-btn>
      <v-btn class="mx-2" v-else text to="/login">Login</v-btn>
    </v-app-bar>

    <v-main>
      <v-container class="pa-4">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import EagleLogoGreenBackground from '@/assets/EagleLogoGreenBackground.png'

const isAuthenticated = ref(false)
const isAdmin = ref(false)
const router = useRouter()

onMounted(() => {
  const token = localStorage.getItem('token')
  isAuthenticated.value = !!token
  // TODO: Fetch user info to check if admin
})

const logout = () => {
  localStorage.removeItem('token')
  isAuthenticated.value = false
  isAdmin.value = false
  router.push('/')
}
</script>

<style scoped>
.v-application {
  /* Use Rubik for more character; fall back to system fonts */
  font-family: 'Rubik', Inter, Roboto, sans-serif;
  /* All-uppercase style as requested */
  text-transform: uppercase;
  /* Slight letter spacing for readability when uppercased */
  letter-spacing: 0.02em;
}
</style>

<style>
.v-toolbar-title, .v-card-title, .text-h5 {
  font-family: 'Permanent Marker', 'Rubik', Inter, Roboto, sans-serif;
  text-transform: none !important;
  letter-spacing: 0;
}
</style>
