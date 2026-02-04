import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import Login from './pages/Login.vue'
import Register from './pages/Register.vue'
import CreateEvent from './pages/CreateEvent.vue'
import Events from './pages/Events.vue'
import Users from './pages/Users.vue'
import { useAuthStore } from './stores/auth'
import { watch } from 'vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
    {
      path: '/create-event',
      name: 'CreateEvent',
      component: CreateEvent,
      meta: { requiresAuth: true },
    },
    {
      path: '/admin/users',
      name: 'Users',
      component: Users,
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/events',
      name: 'Events',
      component: Events,
    }
  ],
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  // 1. Wait for auth hydration
  if (!auth.isHydrated) {
    const stop = watch(
      () => auth.isHydrated,
      () => {
        stop()
        next(to)
      }
    )
    return
  }

  // 2. Auth required
  if (to.meta.requiresAuth && !auth.token) {
    next({ path: '/login', replace: true })
    return
  }

  // 3. Admin required
  if (to.meta.requiresAdmin && !auth.user?.is_admin) {
    next({ path: '/', replace: true })
    return
  }

  // 4. Prevent logged-in users from accessing login/register
  if ((to.name === 'Login' || to.name === 'Register') && auth.token) {
    next({ path: '/', replace: true })
    return
  }

  next()
})

export default router
