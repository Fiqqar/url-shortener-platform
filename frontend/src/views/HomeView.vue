<script setup lang="ts">
import AnalyticsCard from '../components/AnalyticsCard.vue'
import ShortUrlResult from '../components/ShortUrlResult.vue'
import UrlForm from '../components/UrlForm.vue'
import { useUrlShortener } from '../composables/useUrlShortener'

const s = useUrlShortener()

async function onSubmit() {
  await s.submit()
  if (s.result.value) {
    await s.loadAnalytics(s.result.value.code)
  }
}
</script>

<template>
  <main class="page">
    <h1>URL Shortener</h1>
    <p class="lede">Paste a long URL, get a short link, copy it and track clicks.</p>
    <div class="card form-card">
      <UrlForm
        v-model="s.inputUrl.value"
        :loading="s.loading.value"
        :error="s.error.value"
        @submit="onSubmit"
      />
    </div>
    <ShortUrlResult
      v-if="s.result.value"
      :result="s.result.value"
      :copied="s.copied.value"
      @copy="s.copyResult()"
    />
    <AnalyticsCard :analytics="s.analytics.value" />
    <p class="inline-link">
      <RouterLink
        :to="s.result.value ? { path: '/analytics', query: { code: s.result.value.code } } : '/analytics'"
        >Check analytics by code →</RouterLink
      >
    </p>
  </main>
</template>
