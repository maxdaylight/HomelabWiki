<template>
  <div class="edit-page-view">
    <div class="edit-page-header">
      <h1>Edit Page</h1>
    </div>
    
    <div class="edit-page-content">
      <div class="edit-placeholder">
        <p>Page editing functionality will be implemented here.</p>
        <p>This will allow users to edit existing wiki pages.</p>
        <router-link to="/pages" class="back-button">← Back to Pages</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditPageView'
}
</script>

<style lang="scss" scoped>
.edit-page-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.edit-page-header {
  margin-bottom: 2rem;
  
  h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
  }
}

.edit-page-content {
  .edit-placeholder {
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
