<template>
  <div class="page-view">
    <div class="page-header">
      <h1>Page View</h1>
    </div>
    
    <div class="page-content">
      <div class="page-placeholder">
        <p>Individual page view functionality will be implemented here.</p>
        <p>This will display the selected wiki page content.</p>
        <router-link to="/pages" class="back-button">← Back to Pages</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageView'
}
</script>

<style lang="scss" scoped>
.page-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  margin-bottom: 2rem;
  
  h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
  }
}

.page-content {
  .page-placeholder {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 3rem;
    text-align: center;
    
    p {
      color: #6b7280;
      margin-bottom: 1rem;
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
