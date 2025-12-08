<template>
  <div class="calendar">
    <v-row align="center" justify="space-between" class="mb-4">
      <v-btn icon @click="prevMonth" aria-label="Previous month">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
      <div class="text-h6">{{ monthLabel }}</div>
      <v-btn icon @click="nextMonth" aria-label="Next month">
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
    </v-row>

    <div class="weekday-headers">
      <div class="weekday" v-for="d in weekdayNames" :key="d">{{ d }}</div>
    </div>

    <div class="days-grid">
      <div
        v-for="day in days"
        :key="day.dateKey"
        class="day-cell"
        :class="{ 'not-in-month': !day.inMonth, today: day.isToday }"
        @click="onDayClick(day)"
      >
        <v-card outlined class="day-card">
          <div class="day-header">
            <div class="day-number">{{ day.date.getDate() }}</div>
          </div>
          <div class="events-list">
            <div
              v-for="ev in day.events"
              :key="ev.id"
              class="event-pill"
              @click.stop="() => $emit('event-click', ev)"
              :title="ev.title"
            >
              {{ ev.title }}
            </div>
          </div>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps, defineEmits, ref, watch } from 'vue'

type CalendarEvent = { id: string | number; title: string; date: string }

const props = defineProps<{
  events?: CalendarEvent[]
  year?: number
  month?: number // 0-indexed
}>()

const emit = defineEmits<{
  (e: 'event-click', ev: CalendarEvent): void
  (e: 'day-click', date: string): void
}>()

const today = new Date()
const activeYear = ref(props.year ?? today.getFullYear())
const activeMonth = ref(props.month ?? today.getMonth())

watch(() => props.year, (v) => { if (v !== undefined) activeYear.value = v })
watch(() => props.month, (v) => { if (v !== undefined) activeMonth.value = v })

const weekdayNames = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

function startOfMonth(year: number, month: number) {
  return new Date(year, month, 1)
}

function endOfMonth(year: number, month: number) {
  return new Date(year, month + 1, 0)
}

function padZero(n: number) { return n < 10 ? `0${n}` : `${n}` }

function dateKey(d: Date) {
  return `${d.getFullYear()}-${padZero(d.getMonth()+1)}-${padZero(d.getDate())}`
}

function buildDays(year: number, month: number) {
  const start = startOfMonth(year, month)
  const end = endOfMonth(year, month)
  const startWeekday = start.getDay()
  const totalDays = end.getDate()

  const days: Array<any> = []

  // previous month's tail
  for (let i = 0; i < startWeekday; i++) {
    const d = new Date(year, month, 1 - (startWeekday - i))
    days.push({ date: d, inMonth: false, dateKey: dateKey(d), events: [], isToday: isSameDay(d, today) })
  }

  // current month
  for (let day = 1; day <= totalDays; day++) {
    const d = new Date(year, month, day)
    days.push({ date: d, inMonth: true, dateKey: dateKey(d), events: [], isToday: isSameDay(d, today) })
  }

  // next month's head to fill to full weeks (7 columns)
  while (days.length % 7 !== 0) {
    const last = days[days.length - 1].date
    const d = new Date(last.getFullYear(), last.getMonth(), last.getDate() + 1)
    days.push({ date: d, inMonth: false, dateKey: dateKey(d), events: [], isToday: isSameDay(d, today) })
  }

  // attach events
  const evMap = new Map<string, CalendarEvent[]>()
  ;(props.events ?? []).forEach((ev) => {
    evMap.set(ev.date, (evMap.get(ev.date) ?? []).concat(ev))
  })

  for (const d of days) {
    d.events = evMap.get(d.dateKey) ?? []
  }

  return days
}

function isSameDay(a: Date, b: Date) {
  return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate()
}

const days = computed(() => buildDays(activeYear.value, activeMonth.value))

const monthLabel = computed(() => {
  const d = new Date(activeYear.value, activeMonth.value, 1)
  return d.toLocaleString(undefined, { month: 'long', year: 'numeric' })
})

function prevMonth() {
  if (activeMonth.value === 0) { activeMonth.value = 11; activeYear.value -= 1 }
  else activeMonth.value -= 1
}

function nextMonth() {
  if (activeMonth.value === 11) { activeMonth.value = 0; activeYear.value += 1 }
  else activeMonth.value += 1
}

function onDayClick(day: any) {
  emit('day-click', day.dateKey)
}

// no extra refs needed; `weekdayNames` is used in template
</script>

<style scoped>
.calendar {
  width: 100%;
}
.weekday-headers {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  margin-bottom: 8px;
}
.weekday {
  text-align: center;
  font-weight: 600;
  color: rgba(0,0,0,0.7);
}
.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
}
.day-cell {
  min-height: 140px;
}
.day-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  padding: 8px;
}
.day-header {
  display: flex;
  justify-content: flex-end;
}
.day-number {
  font-size: 0.95rem;
  color: rgba(0,0,0,0.8);
}
.not-in-month .day-card {
  opacity: 0.45;
  background: transparent !important;
}
.today .day-card {
  border: 1px solid rgba(0,0,0,0.12);
  background-color: rgba(14,119,3,0.04);
}
.events-list {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.event-pill {
  background: rgba(14,119,3,0.08);
  color: rgba(0,0,0,0.85);
  border-radius: 6px;
  padding: 6px 8px;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>

