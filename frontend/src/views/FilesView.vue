<template>
  <div class="files-view">
    <div class="files-header">
      <h1>Files</h1>
    </div>
    
    <div class="files-content">
      <div class="files-placeholder">
        <p>File management functionality will be implemented here.</p>
        <p>You'll be able to upload, view, and manage your files.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FilesView'
}
</script>

<style lang="scss" scoped>
.files-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.files-header {
  margin-bottom: 2rem;
  
  h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
  }
}

.files-content {
  .files-placeholder {
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
