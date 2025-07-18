<template>
  <div class="create-page-view">
    <div class="create-page-header">
      <h1>Create New Page</h1>
    </div>
    
    <div class="create-page-content">
      <div class="placeholder">
        <p>Page creation functionality will be implemented here.</p>
        <router-link to="/pages" class="back-button">← Back to Pages</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CreatePageView'
}
</script>

<style lang="scss" scoped>
.create-page-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.create-page-header {
  margin-bottom: 2rem;
  
  h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
  }
}

.create-page-content {
  .placeholder {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 3rem;
    text-align: center;
    
    p {
      color: #6b7280;
      margin-bottom: 2rem;
    }
    
    .back-button {
      color: #3b82f6;
      text-decoration: none;
      font-weight: 500;
      
      &:hover {
        text-decoration: underline;
      }
    }
  }
}
</style>
