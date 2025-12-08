<template>
  <v-row align="center" justify="center">
    <v-col cols="12" md="8">
      <v-card class="mx-auto pa-6" elevation="6">
        <v-card-text class="mb-4">
          <Calendar :events="events" @event-click="onEventClick" />
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import Calendar from '@/components/Calendar.vue'
import { ref } from 'vue'

// sample events for demo (dates in YYYY-MM-DD)
const now = new Date()
const year = now.getFullYear()
const month = String(now.getMonth() + 1).padStart(2, '0')

const events = ref([
  { id: 1, title: 'Welcome meeting', date: `${year}-${month}-05` },
  { id: 2, title: 'Study group', date: `${year}-${month}-12` },
  { id: 3, title: 'Club fair', date: `${year}-${month}-21` },
])

function onEventClick(ev: any) {
  alert(`Event clicked: ${ev.title} (${ev.date})`)
}
</script>

<style scoped>
.v-application {
  font-family: Inter, Roboto, sans-serif;
}
</style>
