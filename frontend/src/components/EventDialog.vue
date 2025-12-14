<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="700px">
    <v-card v-if="event">
      <v-card-title>
        <div>
          <div>{{ event.title }}</div>
        </div>
      </v-card-title>
      <v-card-subtitle>
        <div class="mb-2">Created by: {{ event.creator_name }}</div>
      </v-card-subtitle>

      <v-card-text>

        <v-divider />

        <v-row class="mb-2 mt-2">
          <v-col cols="12">
            <div class="section-content" style="white-space: pre-line;">{{ event.description || 'No description' }}</div>
          </v-col>
        </v-row>

        <v-divider />

        <v-row class="py-4" align="center">
          <v-col cols="12" md="6" class="d-flex align-center">
            <v-icon class="me-3" size="20">mdi-calendar</v-icon>
            <div>
              <div class="section-content">{{ formatRange(event.start_time, event.end_time) }}</div>
            </div>
          </v-col>

          <v-col cols="12" md="6" class="d-flex align-center">
            <v-icon class="me-3" size="20">mdi-map-marker</v-icon>
            <div>
              <div class="section-content">{{ event.location || 'No location' }}</div>
            </div>
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="$emit('update:modelValue', false)">Close</v-btn>
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
.section-label { font-weight: 600; color: rgba(0,0,0,0.7); margin-bottom: 6px; }
.section-content { color: rgba(0,0,0,0.87); }
.subtitle-text {
  color: rgba(0,0,0,0.6);
  white-space: normal; /* allow wrapping so the time isn't cut off */
  font-size: 0.9rem;
}
</style>