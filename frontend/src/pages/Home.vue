<template>
  <v-row align="center" justify="center">
    <v-col cols="12" md="8">
      <v-card class="mx-auto pa-6" elevation="6">
        <v-card-text class="mb-4">
          <Calendar :events="eventsStore.events" @event-click="onEventClick" />
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import Calendar from '@/components/Calendar.vue'
import { onMounted } from 'vue'
import { useEventsStore } from '@/stores/events'

const eventsStore = useEventsStore()

onMounted(async () => {
  await eventsStore.fetchEvents()
})

function onEventClick(ev: any) {
  alert(`Event clicked: ${ev.title} (${ev.date ?? ev.start_time})`)
}
</script>

<style scoped>
.v-application {
  font-family: Inter, Roboto, sans-serif;
}
</style>
