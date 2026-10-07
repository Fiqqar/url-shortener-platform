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
  <section class="card result-hero" aria-live="polite">
    <p class="result-label">Short URL ready</p>
    <a class="short-link" :href="result.short_url" target="_blank" rel="noopener">{{
      result.short_url
    }}</a>
    <div class="code-row">
      <code class="code-chip">{{ result.code }}</code>
    </div>
    <p class="target-url" :title="result.target_url">Target: {{ result.target_url }}</p>
    <div class="copy-row">
      <button type="button" class="secondary" @click="$emit('copy')">Copy</button>
      <span v-if="copied" class="copied-hint">Copied!</span>
    </div>
  </section>
</template>
