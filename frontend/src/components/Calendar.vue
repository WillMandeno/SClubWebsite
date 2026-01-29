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
        :events="displayEvents"
        :type="type"
        @click:day="(_, scope) => onDayClickInternal(scope.date)"
      >
        <template #event="{ event }">
          <div
            class="event-chip"
            :class="{ pending: event.pending }"
            @click.stop="onEventClickInternal(event)"
          >
          <span class="event-text">
            {{ event.name }}
          </span>
          <v-icon small v-if="event.pending">mdi-clock-outline</v-icon>
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
              <v-list-item
                v-for="ev in selectedDay.events"
                :key="ev.id"
                @click="onEventClick(ev)"
                :style="{ opacity: ev.pending ? 0.6 : 1 }"
              >
                <v-list-item-content>
                  <v-list-item-title>
                    {{ ev.title }}
                  </v-list-item-title>
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
import { useAuthStore } from '@/stores/auth'

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
const auth = useAuthStore()

function canViewEvent(ev: Event) {
  if (!ev.pending) return true
  if (auth.user?.is_admin) return true
  if (auth.user && ev.created_by === auth.user.id) return true
  return false
}

const displayEvents = computed<VuetifyEvent[]>(() => events.value.filter(v => canViewEvent(v.raw)))

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
  color: ev.pending ? 'grey-lighten-1' : 'secondary'
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

    // Use the computed displayEvents (VuetifyEvent) so visibility rules match the calendar
    const eventsForDay = displayEvents.value.filter(ev => {
      const evStart = ev.start instanceof Date ? ev.start : new Date(ev.start)
      const evEnd = ev.end instanceof Date ? ev.end! : new Date(ev.end!)
      const overlaps = (evStart < dayEnd) && (evEnd > dayStart)
      return overlaps
    }).map(ev => ev.raw)

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
  display: flex;
  align-items: center;
  height: 100%;
  width: 100%;
  padding: 0 6px;
  font-size: 0.75rem;
  gap: 6px;
}

.event-text {
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.event-chip.pending {
  opacity: 0.55;
  background: #ffaa00ff;
}

</style>

