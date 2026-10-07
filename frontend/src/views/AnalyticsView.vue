<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import AnalyticsCard from '../components/AnalyticsCard.vue'
import { getAnalytics } from '../services/api'
import type { AnalyticsResponse } from '../types/api'

const route = useRoute()
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

onMounted(() => {
  const q = route.query.code
  const initial = Array.isArray(q) ? q[0] : q
  if (typeof initial === 'string' && initial.trim()) {
    code.value = initial.trim()
    void lookup()
  }
})
</script>

<template>
  <main class="page">
    <h1>Analytics</h1>
    <p class="lede">Look up clicks for any short code.</p>
    <div class="card form-card">
      <form @submit.prevent="lookup">
        <label for="code-input">Short code</label>
        <div class="form-row">
          <input id="code-input" v-model="code" placeholder="abc123" autocomplete="off" />
          <button type="submit" :disabled="loading">
            {{ loading ? 'Loading…' : 'Lookup' }}
          </button>
        </div>
      </form>
      <p v-if="error" role="alert">{{ error }}</p>
    </div>
    <AnalyticsCard :analytics="analytics" />
    <p class="inline-link">
      <RouterLink to="/">← Back to home</RouterLink>
    </p>
  </main>
</template>
