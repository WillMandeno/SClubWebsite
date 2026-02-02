<template>
  <v-app v-if="!appMounting">
    <v-app-bar color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer" />

      <v-toolbar-title class="d-flex align-center justify-center centered-title">
        <v-icon class="mr-3 mb-1" @click="router.push('/')">
          <v-img :src="EagleLogoGreenBackground" alt="SClub Logo" contain />
        </v-icon>
        <span class="toolbar-title-text" @click="router.push('/')">SClub Calendar</span>
      </v-toolbar-title>
      
    </v-app-bar>

      <v-navigation-drawer v-model="drawer" app temporary>
        <v-list>
          <v-list-item two-line v-if="isAuthenticated">
            <v-list-item-content>
              <div class="d-flex align-center">
                <v-icon class="mr-2">mdi-account-circle</v-icon>
                <v-list-item-title class="user-display-name">{{ userDisplayName }}</v-list-item-title>
                <v-list-item-subtitle class="ml-1" v-if="isAdmin">(Admin)</v-list-item-subtitle>
              </div>
            </v-list-item-content>
          </v-list-item>

          <v-divider v-if="isAuthenticated"/>

          <v-list-item link @click="goTo('/')" class="d-flex align-center">
            <v-list-item-title><b>Home</b></v-list-item-title>
          </v-list-item>

          <v-list-item link @click="goTo('/events')" class="d-flex align-center">
            <v-list-item-title>Events</v-list-item-title>
          </v-list-item>

          <v-list-item link @click="goToCreate" class="d-flex align-center">
            <v-list-item-title>Create Event</v-list-item-title>
          </v-list-item>

          <v-list-item link @click="goTo('/admin/users')" v-if="isAdmin" class="d-flex align-center">
            <v-list-item-title>Users</v-list-item-title>
          </v-list-item>

          <v-list-item link v-if="isAuthenticated" @click="logoutAndClose" class="d-flex align-center">
            <v-list-item-title><b>Logout</b></v-list-item-title>
          </v-list-item>

          <v-list-item link v-if="!isAuthenticated" @click="goTo('/login')" class="d-flex align-center">
            <v-list-item-title><b>Login</b></v-list-item-title>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>

    <v-main>
      <v-container class="pa-4">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
  <v-app v-else>
    <div class="loading-screen">
      <div class="logo-frame">
        <img
          :src="EagleLogoGreenBackground"
          alt="SClub Logo"
          class="logo"
        />
      </div>
    </div>
  </v-app>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import EagleLogoGreenBackground from '@/assets/EagleLogoGreenBackground.png'

const router = useRouter()
const auth = useAuthStore()
const appMounting = ref(true)

const drawer = ref(false)

onMounted(() => {
  auth.init()
  appMounting.value = false
})

const isAuthenticated = computed(() => auth.isHydrated && !!auth.token)
const userDisplayName = computed(() => auth.user?.display_name ?? auth.user?.email ?? '')
const isAdmin = computed(() => !!auth.user?.is_admin)

const logout = () => {
  auth.logout()
  router.push('/')
}

function goTo(path: string) {
  drawer.value = false
  router.push(path)
}

function logoutAndClose() {
  drawer.value = false
  logout()
}

function goToCreate() {
  drawer.value = false
  if (auth.token) router.push('/create-event')
  else router.push('/login')
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
/* Ensure app bar can contain an absolutely-centered title */
.v-app-bar {
  position: relative;
}

/* REMOVE??? */
.centered-title {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* true centering */
  display: flex;
  align-items: center;
  gap: 0.5rem;
  pointer-events: none; /* prevents blocking clicks on nav items under it */
}

.centered-title > * {
  pointer-events: auto; /* restore clickability for children */
}
/*  */

.v-toolbar-title, .v-card-title, .text-h5 {
  font-family: 'Permanent Marker', 'Rubik', Inter, Roboto, sans-serif;
  text-transform: none !important;
  letter-spacing: 0;
}

.loading-screen {
  height: 100vh;
  width: 100vw;
  background-color: rgb(var(--v-theme-primary));;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-frame {
  width: 120px;
  height: 120px;
  border: 4px solid white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo {
  width: 80%;
  height: 80%;
  object-fit: contain;
}

</style>
