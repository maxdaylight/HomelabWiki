<template>
  <div class="pages-view">
    <div class="pages-header">
      <h1>Wiki Pages</h1>
      <router-link to="/pages/create" class="create-button" v-if="canCreate">
        Create New Page
      </router-link>
    </div>
    
    <div class="pages-content">
      <div class="pages-placeholder">
        <p>Pages will appear here once you create some content.</p>
        <p>Click "Create New Page" to get started!</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

export default {
  name: 'PagesView',
  setup() {
    const authStore = useAuthStore()
    
    const canCreate = computed(() => authStore.hasPermission('create'))
    
    return {
      canCreate
    }
  }
}
</script>

<style lang="scss" scoped>
.pages-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.pages-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  
  h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
  }
  
  .create-button {
    background: #10b981;
    color: white;
    text-decoration: none;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    font-weight: 500;
    transition: background-color 0.15s ease-in-out;
    
    &:hover {
      background: #059669;
    }
  }
}

.pages-content {
  .pages-placeholder {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 3rem;
    text-align: center;
    
    p {
      color: #6b7280;
      margin-bottom: 1rem;
      
      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

@media (max-width: 768px) {
  .pages-view {
    padding: 1rem;
  }
  
  .pages-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
    
    h1 {
      font-size: 1.5rem;
    }
  }
  
  .pages-content {
    .pages-placeholder {
      padding: 2rem;
    }
  }
}
</style>
