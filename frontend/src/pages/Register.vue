<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" md="6" lg="4">
        <v-card class="pa-6">
          <v-card-title align="center" class="pb-6">Create Account</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">

              <v-text-field
                v-model="displayName"
                label="Display Name"
                type="text"
                :rules="[rules.required]"
                outlined
                dense
                required
              />
              
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                :rules="[rules.required, rules.email]"
                outlined
                dense
                required
              />

              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                :rules="[rules.required]"
                outlined
                dense
                required
              />

              <v-alert v-if="error" color="error" dense>
                {{ error }}
              </v-alert>

              <div class="mt-6">
                 <v-btn :loading="loading" color="primary" size="large" block type="submit">Create account</v-btn>
                 <v-btn class="mt-3" color="secondary" size="large" block outlined @click="goLogin">Back to login</v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const displayName = ref('')
const email = ref('')
const password = ref('')
const router = useRouter()
const auth = useAuthStore()
const { loading } = storeToRefs(auth)
const error = ref('')

const rules = {
  required: (v: string) => !!v || 'Required',
  email: (v: string) => /\S+@\S+\.\S+/.test(v) || 'Invalid email',
}

const handleRegister = async () => {
  error.value = ''
  try {
    await auth.register(email.value, displayName.value, password.value)
    router.push('/')
  } catch (e) {
    console.error('Login failed:', e)
    error.value = 'Login failed. Check credentials.'
  }
}

const goLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.v-application {
  font-family: Inter, Roboto, sans-serif;
}
</style>
