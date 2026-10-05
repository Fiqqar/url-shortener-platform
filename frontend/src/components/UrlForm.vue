<script setup lang="ts">
defineProps<{
  loading: boolean
  modelValue: string
  error: string | null
}>()

defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'submit'): void
}>()
</script>

<template>
  <form @submit.prevent="$emit('submit')">
    <label for="url-input">Long URL</label>
    <input
      id="url-input"
      :value="modelValue"
      type="url"
      placeholder="https://example.com/some/long/path"
      autocomplete="off"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <button type="submit" :disabled="loading">
      {{ loading ? 'Creating…' : 'Shorten' }}
    </button>
    <p v-if="error" role="alert">{{ error }}</p>
  </form>
</template>
