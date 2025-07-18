<template>
  <div class="settings-view">
    <div class="settings-header">
      <h1>Settings</h1>
    </div>
    
    <div class="settings-content">
      <div class="settings-placeholder">
        <p>Settings functionality will be implemented here.</p>
        <p>Admin users will be able to manage system settings.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsView'
}
</script>

<style lang="scss" scoped>
.settings-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.settings-header {
  margin-bottom: 2rem;
  
  h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
  }
}

.settings-content {
  .settings-placeholder {
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
