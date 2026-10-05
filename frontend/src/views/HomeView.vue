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
  <main>
    <h1>URL Shortener</h1>
    <UrlForm
      v-model="s.inputUrl.value"
      :loading="s.loading.value"
      :error="s.error.value"
      @submit="onSubmit"
    />
    <p v-if="s.loading.value">Loading…</p>
    <ShortUrlResult
      v-if="s.result.value"
      :result="s.result.value"
      :copied="s.copied.value"
      @copy="s.copyResult()"
    />
    <AnalyticsCard :analytics="s.analytics.value" />
    <p>
      <RouterLink to="/analytics">Check analytics by code →</RouterLink>
    </p>
  </main>
</template>
