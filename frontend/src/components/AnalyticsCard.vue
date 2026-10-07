<script setup lang="ts">
import type { AnalyticsResponse } from '../types/api'

defineProps<{
  analytics: AnalyticsResponse | null
}>()
</script>

<template>
  <section class="card analytics-card" aria-live="polite">
    <div v-if="analytics" class="analytics-rows">
      <p><span class="k">Code:</span> {{ analytics.code }}</p>
      <p><span class="k">Clicks:</span> {{ analytics.clicks }}</p>
    </div>
    <p v-else class="empty">No analytics yet — create a link above or look up a code.</p>
  </section>
</template>
