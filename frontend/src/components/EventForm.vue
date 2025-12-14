<template>
  <v-form ref="form" @submit.prevent="handleSubmit">
    <v-text-field
      v-model="title"
      label="Event Title"
      :rules="[rules.required]"
      required
    />

    <v-textarea
      v-model="description"
      label="Description"
      rows="4"
    />

    <!-- Start date & time -->
    <v-row dense>
      <v-col cols="12" sm="6">
        <v-menu v-model="startDateMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
          <template #activator="{ props }">
            <v-text-field v-bind="props" v-model="startDateDisplay" label="Start Date" readonly :rules="[rules.required]" variant="outlined" />
          </template>
          <v-date-picker v-model="startDate" @input="startDateMenu = false" />
        </v-menu>
      </v-col>
      <v-col cols="12" sm="6">
        <v-menu v-model="startTimeMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
          <template #activator="{ props }">
            <v-text-field v-bind="props" v-model="startTime" label="Start Time" readonly :rules="[rules.required]" variant="outlined" />
          </template>
          <v-time-picker v-model="startTime" @change="startTimeMenu = false" />
        </v-menu>
      </v-col>
    </v-row>

    <!-- End date & time -->
    <v-row dense>
      <v-col cols="12" sm="6">
        <v-menu v-model="endDateMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
          <template #activator="{ props }">
            <v-text-field v-bind="props" v-model="endDateDisplay" label="End Date" readonly :rules="[rules.required, validateEndRange]" variant="outlined" />
          </template>
          <v-date-picker v-model="endDate" @input="endDateMenu = false" />
        </v-menu>
      </v-col>
      <v-col cols="12" sm="6">
        <v-menu v-model="endTimeMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
          <template #activator="{ props }">
            <v-text-field v-bind="props" v-model="endTime" label="End Time" readonly :rules="[rules.required, validateEndTime]" variant="outlined" />
          </template>
          <v-time-picker v-model="endTime" @change="endTimeMenu = false" />
        </v-menu>
      </v-col>
    </v-row>

    <v-text-field
      v-model="location"
      label="Location (optional)"
    />

    <v-row justify="center" class="ma-2">
      <v-btn :loading="loading" color="primary" type="submit">{{ mode === 'create' ? 'Create Event' : 'Save Event' }}</v-btn>
    </v-row>
  </v-form>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { Event } from '@/types'

interface Props {
  mode: 'create' | 'edit'
  initialEvent?: Event
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const emit = defineEmits<{
  submit: [data: { title: string; description: string; start_time: string; end_time: string; location: string | null }]
}>()

const form = ref()

const title = ref('')
const description = ref('')
const startDate = ref('')
const startTime = ref('')
const endDate = ref('')
const endTime = ref('')
const startDateMenu = ref(false)
const startTimeMenu = ref(false)
const endDateMenu = ref(false)
const endTimeMenu = ref(false)
const location = ref('')

const rules = {
  required: (v: string) => !!v || 'Required',
}

// Normalize Date objects that some pickers may emit
watch(startDate, (v) => {
  if (v instanceof Date) {
    const y = v.getFullYear()
    const m = String(v.getMonth() + 1).padStart(2, '0')
    const d = String(v.getDate()).padStart(2, '0')
    startDate.value = `${y}-${m}-${d}`
  }
})
watch(endDate, (v) => {
  if (v instanceof Date) {
    const y = v.getFullYear()
    const m = String(v.getMonth() + 1).padStart(2, '0')
    const d = String(v.getDate()).padStart(2, '0')
    endDate.value = `${y}-${m}-${d}`
  }
})

// Validation helpers that use the underlying model values (not the display string)
const validateEndRange = () => {
  // only validate dates (ignore times) and target the end-date field
  if (!endDate.value) return true
  if (!startDate.value) return true
  const [y1, m1, d1] = String(startDate.value).split('-').map(Number)
  const [y2, m2, d2] = String(endDate.value).split('-').map(Number)
  if (![y1, m1, d1, y2, m2, d2].every(n => Number.isFinite(n))) return 'Invalid date'
  const startDateOnly = new Date(y1, m1 - 1, d1)
  const endDateOnly = new Date(y2, m2 - 1, d2)
  if (isNaN(startDateOnly.getTime()) || isNaN(endDateOnly.getTime())) return 'Invalid date'
  return endDateOnly >= startDateOnly || 'End date must be the same or after start date.'
}

const validateEndTime = () => {
  // only validate times when dates are equal; otherwise leave to the date rule
  if (!endTime.value) return true
  if (!startDate.value || !startTime.value || !endDate.value) return true
  const [y1, m1, d1] = String(startDate.value).split('-').map(Number)
  const [y2, m2, d2] = String(endDate.value).split('-').map(Number)
  if (![y1, m1, d1, y2, m2, d2].every(n => Number.isFinite(n))) return 'Invalid date'
  const startDateOnly = new Date(y1, m1 - 1, d1)
  const endDateOnly = new Date(y2, m2 - 1, d2)
  if (isNaN(startDateOnly.getTime()) || isNaN(endDateOnly.getTime())) return 'Invalid date'
  if (endDateOnly > startDateOnly) return true // date is already after start; time irrelevant
  if (endDateOnly < startDateOnly) return true // date rule will show the error on date field
  // dates equal -> compare times
  const [sh, sm] = String(startTime.value).split(':').map(Number)
  const [eh, em] = String(endTime.value).split(':').map(Number)
  if (![sh, sm, eh, em].every(n => Number.isFinite(n))) return 'Invalid time'
  const start = new Date(y1, m1 - 1, d1, sh ?? 0, sm ?? 0)
  const end = new Date(y2, m2 - 1, d2, eh ?? 0, em ?? 0)
  if (isNaN(start.getTime()) || isNaN(end.getTime())) return 'Invalid time'
  return end > start || 'End time must be after start time.'
}

const startDateDisplay = computed({
  get: () => {
    if (!startDate.value) return ''
    const raw = startDate.value instanceof Date ? startDate.value.toISOString().split('T')[0] : String(startDate.value)
    const [y, m, d] = raw.split('-').map(Number)
    if (![y, m, d].every(n => Number.isFinite(n))) return ''
    const date = new Date(y, m - 1, d)
    return date.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' })
  },
  set: () => {}
})

const endDateDisplay = computed({
  get: () => {
    if (!endDate.value) return ''
    const raw = endDate.value instanceof Date ? endDate.value.toISOString().split('T')[0] : String(endDate.value)
    const [y, m, d] = raw.split('-').map(Number)
    if (![y, m, d].every(n => Number.isFinite(n))) return ''
    const date = new Date(y, m - 1, d)
    return date.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' })
  },
  set: () => {}
})

onMounted(() => {
  if (props.mode === 'edit' && props.initialEvent) {
    title.value = props.initialEvent.title
    description.value = props.initialEvent.description || ''
    location.value = props.initialEvent.location || ''
    const start = new Date(props.initialEvent.start_time)
    const sy = start.getFullYear()
    const sm = String(start.getMonth() + 1).padStart(2, '0')
    const sd = String(start.getDate()).padStart(2, '0')
    startDate.value = `${sy}-${sm}-${sd}`
    const sh = String(start.getHours()).padStart(2, '0')
    const smin = String(start.getMinutes()).padStart(2, '0')
    startTime.value = `${sh}:${smin}`
    const end = new Date(props.initialEvent.end_time)
    const ey = end.getFullYear()
    const em = String(end.getMonth() + 1).padStart(2, '0')
    const ed = String(end.getDate()).padStart(2, '0')
    endDate.value = `${ey}-${em}-${ed}`
    const eh = String(end.getHours()).padStart(2, '0')
    const emin = String(end.getMinutes()).padStart(2, '0')
    endTime.value = `${eh}:${emin}`
  }
})

const handleSubmit = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  const toYYYYMMDD = (v: string) => {
    if (/^\d{4}-\d{2}-\d{2}$/.test(v)) return v
    const d = new Date(v)
    if (isNaN(d.getTime())) throw new Error(`Invalid date: ${v}`)
    return d.toISOString().split('T')[0]
  }

  const startISO = new Date(`${toYYYYMMDD(startDate.value)}T${startTime.value}:00`).toISOString()
  const endISO = new Date(`${toYYYYMMDD(endDate.value)}T${endTime.value}:00`).toISOString()

  emit('submit', {
    title: title.value,
    description: description.value,
    start_time: startISO,
    end_time: endISO,
    location: location.value || null,
  })
}
</script>

<style scoped>
</style>