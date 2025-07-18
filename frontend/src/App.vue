<template>
  <div id="app">
    <div v-if="isLoading" class="loading-screen">
      <div class="spinner"></div>
      <p>Loading HomelabWiki...</p>
    </div>
    
    <div v-else-if="!isAuthenticated" class="auth-wrapper">
      <LoginView @login-success="handleLoginSuccess" />
    </div>
    
    <div v-else class="app-layout">
      <Header />
      <div class="main-content">
        <Sidebar />
        <main class="content">
          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Sidebar from '@/components/Sidebar.vue'
import { useAuthStore } from '@/stores/auth'
import LoginView from '@/views/LoginView.vue'
import { computed, onMounted, ref } from 'vue'
import { useToast } from 'vue-toastification'

export default {
  name: 'App',
  components: {
    Header,
    Sidebar,
    LoginView
  },
  setup() {
    const authStore = useAuthStore()
    const toast = useToast()
    const isLoading = ref(true)
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    const handleLoginSuccess = () => {
      toast.success('Welcome to HomelabWiki!')
    }
    
    onMounted(async () => {
      try {
        await authStore.checkAuth()
      } catch (error) {
        console.error('Auth check failed:', error)
        toast.error('Failed to check authentication status')
      } finally {
        isLoading.value = false
      }
    })
    
    return {
      isLoading,
      isAuthenticated,
      handleLoginSuccess
    }
  }
}
</script>

<style lang="scss">
@import '@/styles/globals.scss';

#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  overflow: hidden;
}

.loading-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: var(--color-background);
  color: var(--color-text);
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid var(--color-border);
    border-top: 4px solid var(--color-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }
  
  p {
    font-size: 1.1rem;
    color: var(--color-text-secondary);
  }
}

.auth-wrapper {
  height: 100vh;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
}

.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.content {
  flex: 1;
  overflow: auto;
  padding: 2rem;
  background: var(--color-background);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

// Responsive design
@media (max-width: 768px) {
  .content {
    padding: 1rem;
  }
}
</style>
