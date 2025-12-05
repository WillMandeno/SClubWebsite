<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link v-if="isAdmin" to="/create-event">Create Event</router-link>
      <button v-if="isAuthenticated" @click="logout">Logout</button>
      <router-link v-else to="/login">Login</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const isAuthenticated = ref(false)
const isAdmin = ref(false)
const router = useRouter()

onMounted(() => {
  // Check if user is logged in
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
nav {
  padding: 1rem;
  background: #f0f0f0;
  display: flex;
  gap: 1rem;
}

nav a, button {
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: #333;
  cursor: pointer;
  border: none;
  background: white;
  border-radius: 4px;
}

nav a:hover, button:hover {
  background: #ddd;
}
</style>
