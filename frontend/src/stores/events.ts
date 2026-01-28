import { defineStore } from 'pinia'
import { ref } from 'vue'
import { eventService } from '@/services/api'
import type { Event } from '@/types'
import { useAuthStore } from './auth'

export const useEventsStore = defineStore('events', () => {
  const events = ref<Event[]>([])
  const pendingEvents = ref<Event[]>([])
  const loading = ref(false)

  async function fetchEvents() {
    loading.value = true
    try {
      const res = await eventService.getEvents()
      const data = Array.isArray(res.data) ? res.data : []

      events.value = data.filter((event: Event) => !event.pending)
      pendingEvents.value = data.filter((event: Event) => event.pending)
      return events.value, pendingEvents.value
    } finally {
      loading.value = false
    }
  }

  async function createEvent(payload: any) {
    loading.value = true
    try {
      const auth = useAuthStore()
      const payloadWithPending = { ...payload, pending: auth.user?.is_admin ? false : true }
      const res = await eventService.createEvent(payloadWithPending)
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
    pendingEvents,
    loading,
    fetchEvents,
    createEvent,
    updateEvent,
    deleteEvent,
  }
})
