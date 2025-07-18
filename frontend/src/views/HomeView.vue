<template>
  <div class="home-view">
    <div class="welcome-section">
      <h1>Welcome to HomelabWiki</h1>
      <p>Your personal knowledge base for homelab documentation</p>
    </div>
    
    <div class="quick-actions">
      <div class="action-card">
        <h3>📄 Pages</h3>
        <p>Browse and manage your wiki pages</p>
        <router-link to="/pages" class="action-button">View Pages</router-link>
      </div>
      
      <div class="action-card" v-if="canCreate">
        <h3>➕ Create</h3>
        <p>Create a new wiki page</p>
        <router-link to="/pages/create" class="action-button">Create Page</router-link>
      </div>
      
      <div class="action-card">
        <h3>📁 Files</h3>
        <p>Manage your uploaded files</p>
        <router-link to="/files" class="action-button">View Files</router-link>
      </div>
      
      <div class="action-card">
        <h3>🔍 Search</h3>
        <p>Find content across your wiki</p>
        <router-link to="/search" class="action-button">Search</router-link>
      </div>
    </div>
    
    <div class="recent-section">
      <h2>Recent Pages</h2>
      <div class="recent-placeholder">
        <p>Recent pages will appear here once you create some content.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

export default {
  name: 'HomeView',
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
.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.welcome-section {
  text-align: center;
  margin-bottom: 3rem;
  
  h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 1rem;
  }
  
  p {
    font-size: 1.25rem;
    color: #6b7280;
    margin: 0;
  }
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.action-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  transition: transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }
  
  h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 1rem;
  }
  
  p {
    color: #6b7280;
    margin-bottom: 1.5rem;
  }
  
  .action-button {
    display: inline-block;
    background: #3b82f6;
    color: white;
    text-decoration: none;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    font-weight: 500;
    transition: background-color 0.15s ease-in-out;
    
    &:hover {
      background: #2563eb;
    }
  }
}

.recent-section {
  h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 1rem;
  }
  
  .recent-placeholder {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    
    p {
      color: #6b7280;
      margin: 0;
    }
  }
}

@media (max-width: 768px) {
  .home-view {
    padding: 1rem;
  }
  
  .welcome-section {
    h1 {
      font-size: 2rem;
    }
    
    p {
      font-size: 1rem;
    }
  }
  
  .quick-actions {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .action-card {
    padding: 1.5rem;
  }
}
</style>
