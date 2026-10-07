<script setup lang="ts">
</script>

<template>
  <header class="topbar">
    <RouterLink to="/" class="brand">URL Shortener</RouterLink>
    <nav aria-label="Primary">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/analytics">Analytics</RouterLink>
    </nav>
  </header>
  <RouterView />
</template>
