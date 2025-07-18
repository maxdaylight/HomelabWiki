import { useAuthStore } from '@/stores/auth'
import { createRouter, createWebHistory } from 'vue-router'

// Views
import CreatePageView from '@/views/CreatePageView.vue'
import EditPageView from '@/views/EditPageView.vue'
import FilesView from '@/views/FilesView.vue'
import HomeView from '@/views/HomeView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import PagesView from '@/views/PagesView.vue'
import PageView from '@/views/PageView.vue'
import SearchView from '@/views/SearchView.vue'
import SettingsView from '@/views/SettingsView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: true }
  },
  {
    path: '/pages',
    name: 'pages',
    component: PagesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/pages/create',
    name: 'create-page',
    component: CreatePageView,
    meta: { requiresAuth: true, requiresPermission: 'create' }
  },
  {
    path: '/pages/:slug',
    name: 'page',
    component: PageView,
    meta: { requiresAuth: true }
  },
  {
    path: '/pages/:slug/edit',
    name: 'edit-page',
    component: EditPageView,
    meta: { requiresAuth: true, requiresPermission: 'edit' }
  },
  {
    path: '/files',
    name: 'files',
    component: FilesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/search',
    name: 'search',
    component: SearchView,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView,
    meta: { requiresAuth: true, requiresPermission: 'admin' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Redirect to login (handled by App.vue)
    next(false)
    return
  }
  
  // Check if route requires specific permissions
  if (to.meta.requiresPermission && authStore.isAuthenticated) {
    const hasPermission = authStore.user?.permissions?.[`can_${to.meta.requiresPermission}`] || false
    
    if (!hasPermission) {
      next({ name: 'home' })
      return
    }
  }
  
  next()
})

export default router
