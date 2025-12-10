<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="600px">
    <v-card v-if="event">
      <v-card-title>{{ event.title }}</v-card-title>
      <v-card-subtitle>
        Created by: {{ event.creator_name }}
      </v-card-subtitle>
      <v-card-text class="event-dialog-text">
        <p><strong>Description:</strong></p>
        <p style="white-space: pre-line;">{{ event.description || 'No description' }}</p>
        <p><strong>Date & Time:</strong> {{ formatRange(event.start_time, event.end_time) }}</p>
        <p><strong>Location:</strong> {{ event.location || 'No location' }}</p>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="$emit('update:modelValue', false)">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import type { Event } from '@/types';

interface Props {
  modelValue: boolean
  event?: Event
}

const props = defineProps<Props>()

defineEmits<{
  'update:modelValue': [value: boolean]
}>()

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
      return `${dateS} ${timeS} - ${timeE}`
    }
    return `${dateS} ${timeS} - ${dateE} ${timeE}`
  } catch {
    return `${start} — ${end}`
  }
}

function postProcessAMPM(s: string) {
  return s.replace(/\s?(AM|PM)$/i, (_m, p1) => p1.toLowerCase())
}
</script>

<style scoped>
</style>