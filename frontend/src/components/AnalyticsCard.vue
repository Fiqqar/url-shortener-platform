<script setup lang="ts">
import type { AnalyticsResponse } from '../types/api'

defineProps<{
  analytics: AnalyticsResponse | null
}>()
</script>

<template>
  <section v-if="analytics" aria-live="polite">
    <p>Code: {{ analytics.code }}</p>
    <p>Clicks: {{ analytics.clicks }}</p>
  </section>
</template>
