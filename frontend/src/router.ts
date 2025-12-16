import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import Login from './pages/Login.vue'
import Register from './pages/Register.vue'
import CreateEvent from './pages/CreateEvent.vue'
import Events from './pages/Events.vue'
import Users from './pages/Users.vue'

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
      meta: { requiresAuth: true, requiresAdmin: true },
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
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
