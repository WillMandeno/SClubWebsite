<template>
  <div>
    <v-card class="pa-4">
      <v-card-title class="d-flex align-center justify-space-between">
        Upcoming Events
        <v-btn
          v-if="isAuthenticated"
          icon="mdi-plus"
          color="primary"
          @click="goToCreate"
          variant="tonal"
        />
      </v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item v-for="event in events" :key="event.id" class="event-row position-relative" @click="openViewDialog(event)">
            <v-row class="w-100 align-center" no-gutters>
              <v-col cols="12" class="pl-0 event-left">
                <div class="event-title-text">{{ event.title }}</div>
                <div class="event-range">{{ formatRange(event.start_time, event.end_time) }}</div>
              </v-col>
            </v-row>
            <div class="event-action">
              <v-btn v-if="auth.user && (auth.user.id === event.created_by || auth.user.is_admin)" icon size="small" @click.stop="openEditDialog(event)" title="Edit">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn v-if="auth.user && (auth.user.id === event.created_by || auth.user.is_admin)" icon size ="small" @click.stop="openDeleteDialog(event)" title="Delete">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
          </v-list-item>
        </v-list>
        <div v-if="!events.length">No upcoming events.</div>
      </v-card-text>
    </v-card>
    
    <!-- View Event Dialog -->
    <EventDialog v-model="showViewDialog" :event="selectedEvent" />
    
    <!-- Edit Event Dialog -->
    <v-dialog v-model="showEditDialog" max-width="600px">
      <v-card v-if="selectedEvent">
        <v-card-title>Edit Event</v-card-title>
        <v-card-text>
          <EventForm mode="edit" :initial-event="selectedEvent" @submit="handleSave" />
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showEditDialog = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="500px">
      <v-card>
        <v-card-title>Delete event</v-card-title>
        <v-card-text>
          Are you sure you? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="cancelDelete">Cancel</v-btn>
          <v-btn color="error" @click="confirmDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { eventService } from '@/services/api'
import EventDialog from '@/components/EventDialog.vue'
import EventForm from '@/components/EventForm.vue'
import { Event } from '@/types'

const events = ref<Event[]>([])
const router = useRouter()
const auth = useAuthStore()
const selectedEvent = ref<Event | null>(null)
const showViewDialog = ref(false)
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)
const eventToDelete = ref<Event | null>(null)

const isAuthenticated = computed(() => !!auth.token)

// Format a localized, human-friendly date/time range.
const datePartFormatter = new Intl.DateTimeFormat(undefined, { weekday: 'long', day: 'numeric', month: 'long' })
const timePartFormatter = new Intl.DateTimeFormat(undefined, { hour: 'numeric', minute: '2-digit' })

function formatRange(start: string, end: string) {
  try {
    const s = new Date(start)
    const e = new Date(end)
    if (isNaN(s.getTime()) || isNaN(e.getTime())) return `${start} — ${end}`

    const dateS = datePartFormatter.format(s)
    const dateE = datePartFormatter.format(e)
    const timeS = postProcessAMPM(timePartFormatter.format(s))
    const timeE = postProcessAMPM(timePartFormatter.format(e))

    if (dateS === dateE) {
      // Same day: 'Wednesday, 6 December 12:30pm - 11:00pm'
      return `${dateS} ${timeS} - ${timeE}`
    }
    // Different days: 'Wednesday, 6 December 12:30pm - Thursday, 7 December 11:00pm'
    return `${dateS} ${timeS} - ${dateE} ${timeE}`
  } catch {
    return `${start} — ${end}`
  }
}

function postProcessAMPM(s: string) {
  // normalize AM/PM to lowercase and remove space before am/pm
  return s.replace(/\s?(AM|PM)$/i, (_m, p1) => p1.toLowerCase())
}

function openViewDialog(event: Event) {
  selectedEvent.value = event
  showViewDialog.value = true
}

function openEditDialog(event: Event) {
  selectedEvent.value = event
  showEditDialog.value = true
}

function openDeleteDialog(event: Event) {
  eventToDelete.value = event
  showDeleteDialog.value = true
}

function cancelDelete() {
  eventToDelete.value = null
  showDeleteDialog.value = false
}

async function confirmDelete() {
  const ev = eventToDelete.value
  if (!ev) return
  try {
    await eventService.deleteEvent(ev.id)
    events.value = events.value.filter(e => e.id !== ev.id)
    showDeleteDialog.value = false
    eventToDelete.value = null
  } catch (e: any) {
    console.error('Failed to delete event', e)
    const errorMessage = e.response?.data?.message || e.response?.data?.detail || e.message || 'Failed to delete event.'
    alert(`Error: ${errorMessage}`)
  }
}

function goToCreate() {
  router.push('/create-event')
}

async function handleSave(data: { title: string; description: string; start_time: string; end_time: string; location: string | null }) {
  if (!selectedEvent.value) return
  try {
    await eventService.updateEvent(selectedEvent.value.id, data)
    await fetchEvents()
    showEditDialog.value = false
  } catch (e) {
    console.error('Failed to update event', e)
    alert('Failed to save event. Please try again.')
  }
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

/* Ensure each event row doesn't wrap so the action/button stays right-aligned */
.event-row {
  /* reduce default padding so row content fits better */
  padding-top: 8px;
  padding-bottom: 8px;
  cursor: pointer;
}

.event-title-text {
  font-weight: 600;
}

.event-range {
  color: rgba(0,0,0,0.6);
  white-space: normal; /* allow wrapping so the time isn't cut off */
  font-size: 0.9rem;
}

.event-row {
  display: flex !important;
  align-items: center !important;
}
.event-row > .v-list-item__content, .event-row > .v-list-item-content, .event-row .event-title {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  min-width: 0;
}
.event-row > .v-list-item__action, .event-row > .v-list-item-action, .event-row .v-list-item-action {
  margin-left: auto;
  display: flex;
  align-items: center;
}

/* Reserve space on the left content so the absolutely-positioned action doesn't overlap */
.event-left {
  padding-right: 64px;
}

.event-action {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
}
.event-action .v-btn {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  min-width: 40px;
  height: 40px;
  transition: background 0.2s ease, border-radius 0.2s ease;
}
.event-action .v-btn:hover {
  background: rgba(0,0,0,0.1) !important;
  border-radius: 50% !important;
}
</style>
