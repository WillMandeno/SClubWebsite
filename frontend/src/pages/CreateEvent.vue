<template>
  <div v-if="!isAdmin" class="text-center">
    <v-alert type="error">You are not authorized to create events.</v-alert>
  </div>
  <div v-else>
    <v-container class="create-event" fluid>
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card class="pa-6 text-center">
            <div class="sjc-title" style="font-size: 1.75rem; margin-bottom: 1rem">Create Event</div>
            <EventForm mode="create" :loading="loading" @submit="handleCreateEvent" />
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useEventsStore } from '@/stores/events'
import { storeToRefs } from 'pinia'
import EventForm from '@/components/EventForm.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const isAdmin = computed(() => auth.user?.is_admin === true)

const router = useRouter()
const events = useEventsStore()
const { loading } = storeToRefs(events)

const handleCreateEvent = async (data: { title: string; description: string; start_time: string; end_time: string; location: string | null }) => {
  try {
    await events.createEvent(data)
    router.push('/events')
  } catch (error) {
    console.error('Failed to create event:', error)
    alert('Failed to create event: ' + (error instanceof Error ? error.message : String(error)))
  }
}
</script>

<style scoped>
.create-event {
  padding-top: 2rem;
}

.sjc-title {
  font-family: 'Bungee', Rubik, Inter, sans-serif;
  text-transform: none;
  letter-spacing: 0;
}
</style>
