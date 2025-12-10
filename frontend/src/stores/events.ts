import { defineStore } from 'pinia'
import { ref } from 'vue'
import { eventService } from '@/services/api'
import type { Event } from '@/types'

export const useEventsStore = defineStore('events', () => {
  const events = ref<Event[]>([])
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
    loading.value = true
    try {
      const res = await eventService.createEvent(payload)
      await fetchEvents()
      return res
    } finally {
        loading.value = false
    }

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
