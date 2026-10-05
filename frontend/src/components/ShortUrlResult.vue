<script setup lang="ts">
import type { CreateUrlResponse } from '../types/api'

defineProps<{
  result: CreateUrlResponse
  copied: boolean
}>()

defineEmits<{
  (e: 'copy'): void
}>()
</script>

<template>
  <section aria-live="polite">
    <p>Short URL:</p>
    <a :href="result.short_url" target="_blank" rel="noopener">{{
      result.short_url
    }}</a>
    <p>Target: {{ result.target_url }}</p>
    <button type="button" @click="$emit('copy')">Copy</button>
    <span v-if="copied">Copied!</span>
  </section>
</template>
