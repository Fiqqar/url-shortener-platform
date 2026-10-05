<script setup lang="ts">
import { ref } from 'vue'
import AnalyticsCard from '../components/AnalyticsCard.vue'
import { getAnalytics } from '../services/api'
import type { AnalyticsResponse } from '../types/api'

const code = ref('')
const analytics = ref<AnalyticsResponse | null>(null)
const error = ref<string | null>(null)
const loading = ref(false)

async function lookup() {
  error.value = null
  analytics.value = null
  const trimmed = code.value.trim()
  if (!trimmed) {
    error.value = 'Code cannot be empty.'
    return
  }
  loading.value = true
  try {
    analytics.value = await getAnalytics(trimmed)
  } catch (e) {
    error.value =
      e && typeof e === 'object' && 'message' in e
        ? String((e as { message: unknown }).message)
        : 'Failed to load analytics.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main>
    <h1>Analytics</h1>
    <form @submit.prevent="lookup">
      <label for="code-input">Short code</label>
      <input id="code-input" v-model="code" placeholder="abc123" autocomplete="off" />
      <button type="submit" :disabled="loading">
        {{ loading ? 'Loading…' : 'Lookup' }}
      </button>
    </form>
    <p v-if="error" role="alert">{{ error }}</p>
    <AnalyticsCard :analytics="analytics" />
    <p>
      <RouterLink to="/">← Back to home</RouterLink>
    </p>
  </main>
</template>
