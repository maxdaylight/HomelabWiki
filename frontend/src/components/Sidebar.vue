<template>
  <aside class="app-sidebar">
    <nav class="sidebar-nav">
      <router-link to="/" class="nav-item">
        <span class="nav-icon">🏠</span>
        <span class="nav-text">Home</span>
      </router-link>
      
      <router-link to="/pages" class="nav-item">
        <span class="nav-icon">📄</span>
        <span class="nav-text">Pages</span>
      </router-link>
      
      <router-link to="/pages/create" class="nav-item" v-if="canCreate">
        <span class="nav-icon">➕</span>
        <span class="nav-text">Create Page</span>
      </router-link>
      
      <router-link to="/files" class="nav-item">
        <span class="nav-icon">📁</span>
        <span class="nav-text">Files</span>
      </router-link>
      
      <router-link to="/search" class="nav-item">
        <span class="nav-icon">🔍</span>
        <span class="nav-text">Search</span>
      </router-link>
      
      <router-link to="/settings" class="nav-item" v-if="isAdmin">
        <span class="nav-icon">⚙️</span>
        <span class="nav-text">Settings</span>
      </router-link>
    </nav>
  </aside>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

export default {
  name: 'Sidebar',
  setup() {
    const authStore = useAuthStore()
    
    const canCreate = computed(() => authStore.hasPermission('create'))
    const isAdmin = computed(() => authStore.isAdmin)
    
    return {
      canCreate,
      isAdmin
    }
  }
}
</script>

<style lang="scss" scoped>
.app-sidebar {
  width: 16rem;
  background: white;
  border-right: 1px solid #e5e7eb;
  height: 100%;
  overflow-y: auto;
}

.sidebar-nav {
  padding: 1rem 0;
  
  .nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1.5rem;
    color: #6b7280;
    text-decoration: none;
    transition: all 0.15s ease-in-out;
    
    &:hover {
      background: #f3f4f6;
      color: #374151;
    }
    
    &.router-link-active {
      background: #eff6ff;
      color: #3b82f6;
      border-right: 3px solid #3b82f6;
    }
    
    .nav-icon {
      font-size: 1.25rem;
      width: 1.5rem;
      text-align: center;
    }
    
    .nav-text {
      font-weight: 500;
      font-size: 0.875rem;
    }
  }
}

@media (max-width: 768px) {
  .app-sidebar {
    width: 12rem;
  }
  
  .sidebar-nav {
    .nav-item {
      padding: 0.75rem 1rem;
      
      .nav-text {
        font-size: 0.8rem;
      }
    }
  }
}
</style>
