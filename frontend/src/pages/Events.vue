<template>
  <div>
    <v-card class="pa-4">
      <v-card-title>
        Upcoming Events
      </v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item v-for="event in events" :key="event.id">
            <v-list-item-content>
              <v-list-item-title>{{ event.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ formatDate(event.start_time) }} — {{ formatDate(event.end_time) }}</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn text @click="gotoEvent(event.id)">View</v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
        <div v-if="!events.length">No upcoming events.</div>
      </v-card-text>
    </v-card>
    <v-btn v-if="isAuthenticated" class="mt-4" color="primary" @click="goToCreate">Create Event</v-btn>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { eventService } from '@/services/api'

const events = ref<any[]>([])
const router = useRouter()
const auth = useAuthStore()

const isAuthenticated = computed(() => !!auth.token)

function formatDate(dt: string) {
  try {
    return new Date(dt).toLocaleString()
  } catch {
    return dt
  }
}

function gotoEvent(id: number) {
  router.push(`/events/${id}`)
}

function goToCreate() {
  router.push('/create-event')
}

async function fetchEvents() {
  try {
    const res = await eventService.getEvents()
    events.value = res.data || []
  } catch (e) {
    console.error('Failed to fetch events', e)
  }
}

onMounted(() => {
  fetchEvents()
})
</script>

<style scoped>
.user-display-name {
  text-transform: none;
}
</style>
