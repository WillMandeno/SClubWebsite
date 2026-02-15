<template>
  <v-container class="pa-4" fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="pa-6 text-center">
          <div class="sjc-title" style="font-size: 1.75rem; margin-bottom: 1rem">
            Edit Profile
          </div>

          <!-- Profile Form -->
          <v-form ref="form" @submit.prevent="handleProfileSubmit">
            <v-text-field
              v-model="displayName"
              label="Display Name"
              :rules="[rules.required]"
              required
            />
            <v-text-field
              v-model="email"
              label="Email"
              :rules="[rules.required, rules.email]"
              required
            />
            <v-text-field
              v-model="role"
              label="Role"
              readonly
            />

            <v-row justify="center" class="ma-2">
              <v-btn :loading="loading" color="primary" type="submit">
                Save Profile
              </v-btn>
            </v-row>
          </v-form>

          <!-- Alerts -->
          <v-alert type="success" class="mt-4" v-if="successMessage">
            {{ successMessage }}
          </v-alert>
          <v-alert type="error" class="mt-3" v-if="errorMessage">
            {{ errorMessage }}
          </v-alert>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const auth = useAuthStore()
const { loading } = storeToRefs(auth)

const form = ref()

// Profile fields
const displayName = ref('')
const email = ref('')
const role = ref('General User')

// Success / error messages
const successMessage = ref('')
const errorMessage = ref('')

// Validation rules
const rules = {
  required: (v: string) => !!v || 'Required',
  email: (v: string) => /^\S+@\S+\.\S+$/.test(v) || 'Invalid email',
}

onMounted(() => {
  if (auth.user) {
    displayName.value = auth.user.display_name ?? ''
    email.value = auth.user.email ?? ''
    role.value = auth.user.is_admin ? 'Admin' : 'General User'
  }
})

function showMessage(refVar: typeof successMessage, msg: string) {
  refVar.value = msg
  setTimeout(() => (refVar.value = ''), 5000)
}

const handleProfileSubmit = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  // Clear previous messages
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const res = await auth.updateProfile({
      displayName: displayName.value,
      email: email.value,
    })
    showMessage(successMessage, 'Profile updated successfully!')
    console.log('Profile updated', res.data)
  } catch (err: any) {
    const msg =
      err.response?.status === 400
        ? err.response.data.detail
        : 'Something went wrong'
    showMessage(errorMessage, msg)
  }
}
</script>

<style scoped></style>
