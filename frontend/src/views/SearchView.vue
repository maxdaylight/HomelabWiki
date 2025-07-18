<template>
  <div class="search-view">
    <div class="search-header">
      <h1>Search</h1>
    </div>
    
    <div class="search-content">
      <div class="search-placeholder">
        <p>Search functionality will be implemented here.</p>
        <p>You'll be able to search across all wiki content and files.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchView'
}
</script>

<style lang="scss" scoped>
.search-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.search-header {
  margin-bottom: 2rem;
  
  h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
  }
}

.search-content {
  .search-placeholder {
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
</style>
