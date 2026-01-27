<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>
              Users
            </v-card-title>
            <v-card-text>
              <div v-if="!isAdmin" class="text-center">
                <v-alert type="error">You are not authorized to view this page.</v-alert>
              </div>

              <div v-else>
                <v-data-table :items="users" :headers="headers" class="elevation-1">
                  <template #item.is_admin="{ item }">
                    <v-switch v-model="item.is_admin_local" :disabled="item.id === auth.user?.id || auth.user?.email === 'willmandeno@gmail.com'" @change="toggleAdmin(item)" :label="item.is_admin_local ? 'Admin' : 'User'" hide-details dense />
                  </template>

                  <template #item.actions="{ item }">
                    <v-btn color="error" variant="tonal" small :disabled="item.id === auth.user?.id || auth.user?.email === 'willmandeno@gmail.com'" @click="confirmDelete(item)">Delete</v-btn>
                  </template>
                </v-data-table>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-dialog v-model="showDeleteDialog" max-width="500">
      <v-card>
        <v-card-title>Confirm delete</v-card-title>
        <v-card-text>Delete user "{{ userToDelete?.display_name || userToDelete?.email }}" and all their events?</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showDeleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="doDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { adminService } from '@/services/api'

const auth = useAuthStore()

const isAdmin = computed(() => auth.user?.is_admin === true)

const users = ref<Array<any>>([])
const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Display name', key: 'display_name' },
  { title: 'Email', key: 'email' },
  { title: 'Created', key: 'created_at_display' },
  { title: 'Admin', key: 'is_admin' },
  { title: 'Actions', key: 'actions' },
]

const showDeleteDialog = ref(false)
const userToDelete = ref<any | null>(null)

function formatCreatedAt(dateStr: string | undefined) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return ''
  // Use DD/MM/YYYY HH:MM (24-hour) for non-US formatting
  const dd = String(d.getDate()).padStart(2, '0')
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const yyyy = d.getFullYear()
  const hh = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  return `${dd}/${mm}/${yyyy} ${hh}:${min}`
}

async function loadUsers() {
  try {
    const res = await adminService.getUsers()
    // normalize items for v-data-table
    users.value = res.data.map((u: any) => ({
      ...u,
      is_admin_local: u.is_admin,
      display_name: u.display_name ?? u.displayName ?? u.username ?? '',
      created_at_display: formatCreatedAt(u.created_at),
    }))
  } catch (e) {
    console.error(e)
  }
}

function confirmDelete(u: any) {
  userToDelete.value = u
  showDeleteDialog.value = true
}

async function doDelete() {
  if (!userToDelete.value) return
  try {
    await adminService.deleteUser(userToDelete.value.id)
    showDeleteDialog.value = false
    userToDelete.value = null
    await loadUsers()
  } catch (e) {
    console.error(e)
    showDeleteDialog.value = false
  }
}

async function toggleAdmin(item: any) {
  try {
    await adminService.setUserAdmin(item.id, item.is_admin_local)
    // refresh list to reflect any server-side formatting
    await loadUsers()
  } catch (e) {
    console.error(e)
    // revert toggle on error
    item.is_admin_local = !item.is_admin_local
  }
}

watch(isAdmin, (v) => {
  if (v) void loadUsers()
}, { immediate: true })
</script>

<style scoped>
</style>
