<template>
  <header class="app-header">
    <div class="header-content">
      <div class="header-left">
        <h1 class="app-title">HomelabWiki</h1>
      </div>
      
      <div class="header-right">
        <div class="user-menu">
          <span class="user-name">{{ user?.display_name || user?.username }}</span>
          <button @click="handleLogout" class="logout-button">
            Logout
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

export default {
  name: 'Header',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const toast = useToast()
    
    const user = computed(() => authStore.user)
    
    const handleLogout = async () => {
      try {
        await authStore.logout()
        toast.success('Logged out successfully')
        router.push('/')
      } catch (error) {
        toast.error('Logout failed')
      }
    }
    
    return {
      user,
      handleLogout
    }
  }
}
</script>

<style lang="scss" scoped>
.app-header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 2rem;
  height: 4rem;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.header-left {
  .app-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
  }
}

.header-right {
  .user-menu {
    display: flex;
    align-items: center;
    gap: 1rem;
    
    .user-name {
      font-weight: 500;
      color: #374151;
    }
    
    .logout-button {
      background: #ef4444;
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      font-size: 0.875rem;
      cursor: pointer;
      transition: background-color 0.15s ease-in-out;
      
      &:hover {
        background: #dc2626;
      }
    }
  }
}

@media (max-width: 768px) {
  .app-header {
    padding: 0 1rem;
  }
  
  .header-left {
    .app-title {
      font-size: 1.25rem;
    }
  }
  
  .header-right {
    .user-menu {
      .user-name {
        display: none;
      }
    }
  }
}
</style>
