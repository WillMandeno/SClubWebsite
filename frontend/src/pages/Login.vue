<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
    <!-- TODO: Add register link -->
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/api'

const email = ref('')
const password = ref('')
const router = useRouter()

const handleLogin = async () => {
  try {
    const response = await authService.login(email.value, password.value)
    localStorage.setItem('token', response.data.access_token)
    router.push('/')
  } catch (error) {
    console.error('Login failed:', error)
  }
}
</script>

<style scoped>
.login {
  padding: 2rem;
  max-width: 400px;
  margin: 2rem auto;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input, button {
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background: #007bff;
  color: white;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}
</style>
