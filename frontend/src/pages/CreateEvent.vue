<template>
  <v-container class="create-event" fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="pa-6 text-center">
          <div class="sjc-title" style="font-size: 1.75rem; margin-bottom: 1rem">Create Event</div>

          <v-form @submit.prevent="handleCreateEvent">
            <v-text-field
              v-model="title"
              label="Event Title"
              required
            />

            <v-textarea
              v-model="description"
              label="Description"
              rows="4"
            />

            <!-- Start date & time -->
            <v-row>
              <v-col cols="12" sm="6">
                <v-menu v-model="startDateMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
                  <template #activator="{ props }">
                    <v-text-field v-bind="props" v-model="startDate" label="Start Date" readonly required />
                  </template>
                  <v-date-picker v-model="startDate" @input="startDateMenu = false" />
                </v-menu>
              </v-col>
              <v-col cols="12" sm="6">
                <v-menu v-model="startTimeMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
                  <template #activator="{ props }">
                    <v-text-field v-bind="props" v-model="startTime" label="Start Time" readonly required />
                  </template>
                  <v-time-picker v-model="startTime" @change="startTimeMenu = false" />
                </v-menu>
              </v-col>
            </v-row>

            <!-- End date & time -->
            <v-row>
              <v-col cols="12" sm="6">
                <v-menu v-model="endDateMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
                  <template #activator="{ props }">
                    <v-text-field v-bind="props" v-model="endDate" label="End Date" readonly required />
                  </template>
                  <v-date-picker v-model="endDate" @input="endDateMenu = false" />
                </v-menu>
              </v-col>
              <v-col cols="12" sm="6">
                <v-menu v-model="endTimeMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
                  <template #activator="{ props }">
                    <v-text-field v-bind="props" v-model="endTime" label="End Time" readonly required />
                  </template>
                  <v-time-picker v-model="endTime" @change="endTimeMenu = false" />
                </v-menu>
              </v-col>
            </v-row>

            <v-text-field
              v-model="location"
              label="Location (optional)"
            />

            <v-row justify="center" class="mt-4">
              <v-btn :loading="loading" :disabled="loading" color="primary" type="submit">Create Event</v-btn>
            </v-row>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useEventsStore } from '@/stores/events'
import { storeToRefs } from 'pinia'

const title = ref('')
const description = ref('')
const startDate = ref('')
const startTime = ref('')
const endDate = ref('')
const endTime = ref('')
const startDateMenu = ref(false)
const startTimeMenu = ref(false)
const endDateMenu = ref(false)
const endTimeMenu = ref(false)
const location = ref('')
const router = useRouter()
const events = useEventsStore()
const { loading } = storeToRefs(events)

// Using Vuetify default bindings for pickers — no custom display helpers required

const handleCreateEvent = async () => {
  try {
    // basic validation
    const rawStart = startDate.value
    const rawEnd = endDate.value
    const isEmpty = (v: any) => v === null || v === undefined || String(v).trim() === ''
    if (isEmpty(rawStart)) {
      alert('Please choose a start date')
      return
    }
    if (isEmpty(rawEnd)) {
      alert('Please choose an end date')
      return
    }

    const toYYYYMMDD = (v: any) => {
      // If already in YYYY-MM-DD form
      if (typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v)) return v
      // If string starts with ISO date
      if (typeof v === 'string') {
        const m = String(v).match(/^(\d{4}-\d{2}-\d{2})/) 
        if (m) return m[1]
      }
      // If Date object or other parseable string
      const d = v instanceof Date ? v : new Date(String(v))
      if (isNaN(d.getTime())) throw new Error(`Invalid date value: ${v}`)
      const y = d.getFullYear()
      const m = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${y}-${m}-${day}`
    }

    const makeISO = (dateVal: any, timeStr = '00:00') => {
      const dateOnly = toYYYYMMDD(dateVal)
      const isoStr = `${dateOnly}T${timeStr}`
      const d = new Date(isoStr)
      if (isNaN(d.getTime())) throw new Error(`Invalid date/time: ${isoStr}`)
      return d.toISOString()
    }

    const startISO = makeISO(rawStart, startTime.value || '00:00')
    const endISO = makeISO(rawEnd, endTime.value || '00:00')

    await events.createEvent({
      title: title.value,
      description: description.value,
      start_time: startISO,
      end_time: endISO,
      location: location.value || null,
    })
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
