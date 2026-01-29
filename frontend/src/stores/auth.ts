import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authService } from '@/services/api'

type User = {
	id?: number
	email?: string
	display_name?: string
	is_admin?: boolean
}

export const useAuthStore = defineStore('auth', () => {
	const token = ref<string | null>(localStorage.getItem('token'))
	const user = ref<User | null>(null)
	const loading = ref(false)
	const isHydrated = ref(false)

	function normalizeUser(u: any): User | null {
		if (!u) return null
		return {
			id: u.id,
			email: u.email,
			display_name: u.display_name ?? u.displayName ?? u.username ?? undefined,
			is_admin: u.is_admin ?? u.isAdmin ?? false,
		}
	}

	function setToken(t: string | null) {
		token.value = t
		if (t) localStorage.setItem('token', t)
		else localStorage.removeItem('token')
	}

	async function fetchMe() {
		if (!token.value) return null
		try {
			const res = await authService.getMe()
			user.value = normalizeUser(res.data)
			return user.value
		} catch (e) {
			// token invalid or request failed -> clear auth
			setToken(null)
			user.value = null
			return null
		}
	}

	async function login(email: string, password: string) {
		loading.value = true
		try {
			const res = await authService.login(email, password)
			const t = res.data?.access_token
			if (t) {
				setToken(t)
				await fetchMe()
			}
			return res
		} finally {
			loading.value = false
		}
	}

	async function register(email: string, displayName: string, password: string) {
		loading.value = true
		try {
			const res = await authService.register(email, displayName, password)
			const t = res.data?.access_token
			if (t) {
				setToken(t)
				await fetchMe()
			}
			return res
		} finally {
			loading.value = false
		}
	}

	function logout() {
		setToken(null)
		user.value = null
	}

	async function init() {
		const t = localStorage.getItem('token')
		if (t) {
			token.value = t
			// maybe don't await here; allow app to continue mounting
			await fetchMe()
		}
		isHydrated.value = true
	}

	return {
		token,
		user,
		loading,
		isHydrated,
		setToken,
		fetchMe,
		login,
		register,
		logout,
		init,
	}
})
