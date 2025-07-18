<template>
  <div class="not-found-view">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The page you're looking for doesn't exist.</p>
      <router-link to="/" class="home-button">Go Home</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView'
}
</script>

<style lang="scss" scoped>
.not-found-view {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  
  h1 {
    font-size: 6rem;
    font-weight: 900;
    color: #3b82f6;
    margin-bottom: 1rem;
    line-height: 1;
  }
  
  h2 {
    font-size: 2rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 1rem;
  }
  
  p {
    font-size: 1.125rem;
    color: #6b7280;
    margin-bottom: 2rem;
  }
  
  .home-button {
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
</style>
