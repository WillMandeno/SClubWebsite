import { defineStore } from 'pinia'
import { ref } from 'vue'
import { eventService } from '@/services/api'

type EventItem = {
  id: number | string
  title: string
  description?: string
  start_time?: string
  end_time?: string
  date?: string
  location?: string | null
}

export const useEventsStore = defineStore('events', () => {
  const events = ref<EventItem[]>([])
  const loading = ref(false)

  async function fetchEvents() {
    loading.value = true
    try {
      const res = await eventService.getEvents()
      // assume backend returns an array of events
      events.value = res.data
      return events.value
    } finally {
      loading.value = false
    }
  }

  async function createEvent(payload: any) {
    const res = await eventService.createEvent(payload)
    // refresh list after create
    await fetchEvents()
    return res
  }

  async function updateEvent(id: number | string, payload: any) {
    const res = await eventService.updateEvent(Number(id), payload)
    await fetchEvents()
    return res
  }

  async function deleteEvent(id: number | string) {
    const res = await eventService.deleteEvent(Number(id))
    await fetchEvents()
    return res
  }

  return {
    events,
    loading,
    fetchEvents,
    createEvent,
    updateEvent,
    deleteEvent,
  }
})
