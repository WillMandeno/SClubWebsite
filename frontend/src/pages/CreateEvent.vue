<template>
  <div class="create-event">
    <h1>Create Event</h1>
    <form @submit.prevent="handleCreateEvent">
      <input v-model="title" type="text" placeholder="Event Title" required />
      <textarea v-model="description" placeholder="Description"></textarea>
      <input v-model="startTime" type="datetime-local" required />
      <input v-model="endTime" type="datetime-local" required />
      <input v-model="location" type="text" placeholder="Location (optional)" />
      <button type="submit">Create Event</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useEventsStore } from '@/stores/events'

const title = ref('')
const description = ref('')
const startTime = ref('')
const endTime = ref('')
const location = ref('')
const router = useRouter()
const events = useEventsStore()

const handleCreateEvent = async () => {
  try {
    await events.createEvent({
      title: title.value,
      description: description.value,
      start_time: new Date(startTime.value).toISOString(),
      end_time: new Date(endTime.value).toISOString(),
      location: location.value || null,
    })
    router.push('/')
  } catch (error) {
    console.error('Failed to create event:', error)
  }
}
</script>

<style scoped>
.create-event {
  padding: 2rem;
  max-width: 600px;
  margin: 2rem auto;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input, textarea, button {
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  background: #28a745;
  color: white;
  cursor: pointer;
}

button:hover {
  background: #218838;
}
</style>
