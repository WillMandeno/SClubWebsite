<template>
  <div>
    <v-sheet class="d-flex" tile>
      <v-btn
        class="ma-2"
        variant="text"
        icon
        @click="($refs.calendar as any)?.prev()"
      >
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
      <v-spacer></v-spacer>
      <div class="sjc-title">{{ monthLabel }}</div>
      <v-spacer></v-spacer>
      <v-btn
        class="ma-2"
        variant="text"
        icon
        @click="($refs.calendar as any)?.next()"
      >
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
    </v-sheet>
    <v-sheet height="600">
      <v-calendar
        ref="calendar"
        v-model="value"
        :events="events"
        :type="type"
        @click:day="(_, scope) => onDayClickInternal(scope.date)"
      >
        <template #event="{ event }">
          <div :class="event.pending ? 'pending-event-chip' : 'event-chip'" :title="event.name" @click.stop="onEventClickInternal(event)">
            {{ event.name }}
          </div>
        </template>
      </v-calendar>
    </v-sheet>

    <v-dialog v-model="showDayDialog" max-width="640">
      <v-card v-if="selectedDay">
        <v-card-title>{{ formatDate(selectedDay.date) }}</v-card-title>
        <v-card-subtitle>Events on this day:</v-card-subtitle>
        <v-card-text>
          <div v-if="selectedDay.events.length === 0">No events on this day.</div>
          <div v-else>
            <v-list>
              <v-list-item v-for="ev in selectedDay.events" :key="ev.id" @click="onEventClick(ev)">
                <v-list-item-content>
                  <v-list-item-title>{{ ev.title }}</v-list-item-title>
                  <v-list-item-subtitle v-if="ev.description">{{ ev.description }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showDayDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <EventDialog :event="selectedEvent" v-model="showEventDialog" />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import EventDialog from './EventDialog.vue';
import type { Event } from '@/types';

type VuetifyEvent = { name: string; start: string | Date; end?: string | Date; color?: string; id?: string | number; raw?: any }

const props = defineProps<{
  events?: Event[]
  year?: number
  month?: number
}>()

const type = ref<'month'>('month')
const value = ref('')
const selectedDay = ref<{ date: string; events: Event[] } | null>(null)
const showDayDialog = ref(false)
const selectedEvent = ref<Event | undefined>(undefined)
const showEventDialog = ref(false)

watch(() => props.year, (v) => {
  if (v !== undefined) value.value = `${v}-${String((props.month ?? new Date().getMonth() + 1)).padStart(2, '0')}-01`
})

const events = computed<VuetifyEvent[]>(() => (props.events ?? []).map(ev => ({
  name: ev.title,
  start: new Date(ev.start_time),
  end: new Date(ev.end_time),
  id: ev.id,
  raw: ev,
  pending: !!ev.pending,
  color: 'secondary'
})))

const monthLabel = computed(() => {
  const d = new Date(value.value || new Date())
  return d.toLocaleString(undefined, { month: 'long', year: 'numeric' })
})

const dateFormatter = new Intl.DateTimeFormat('en-GB', { weekday: 'long', day: 'numeric', month: 'long' })

function formatDate(dateStr: string) {
  return dateFormatter.format(new Date(dateStr))
}

function onEventClickInternal(event: any) {
  selectedEvent.value = event.raw
  showEventDialog.value = true
}

function onDayClickInternal(payload: any) {
  const date = payload?.date ?? payload
  const isoDate = (typeof date === 'string') ? date.split('T')[0] : String(date)

  // Build local start/end-of-day boundaries (avoid forcing UTC)
  const dayStart = new Date(isoDate)
  dayStart.setHours(0, 0, 0, 0)
  const dayEnd = new Date(dayStart)
  dayEnd.setDate(dayEnd.getDate() + 1)

  const eventsForDay = (props.events ?? []).filter(e => {
    const evStart = new Date(e.start_time)
    const evEnd = new Date(e.end_time)
    // use strict overlap: event starts before dayEnd and ends after dayStart
    const overlaps = (evStart < dayEnd) && (evEnd > dayStart)
    return overlaps
  })
  
  console.log(`Day ${isoDate}: found ${eventsForDay.length} events`)
  selectedDay.value = { date: isoDate, events: eventsForDay }
  showDayDialog.value = true
}

function onEventClick(ev: any) {
  selectedEvent.value = ev
  showEventDialog.value = true
}
</script>

<style scoped>
.event-chip {
  padding: 4px 8px;
  font-size: 0.75rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  background: '#ffaa00ff'; 
}

.pending-event-chip {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  background: #ffde92;
  opacity: 0.6;
}
</style>

