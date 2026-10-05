import { ref } from 'vue'
import { createShortUrl, getAnalytics } from '../services/api'
import type { AnalyticsResponse, CreateUrlResponse } from '../types/api'

export function isValidHttpUrl(value: string): boolean {
  const trimmed = value.trim()
  if (!trimmed) return false
  try {
    const parsed = new URL(trimmed)
    return parsed.protocol === 'http:' || parsed.protocol === 'https:'
  } catch {
    return false
  }
}

export function useUrlShortener() {
  const inputUrl = ref('')
  const loading = ref(false)
  const result = ref<CreateUrlResponse | null>(null)
  const analytics = ref<AnalyticsResponse | null>(null)
  const error = ref<string | null>(null)
  const copied = ref(false)

  function validate(): string | null {
    const trimmed = inputUrl.value.trim()
    if (!trimmed) return 'URL cannot be empty.'
    if (!isValidHttpUrl(trimmed)) {
      return 'Enter a valid http:// or https:// URL.'
    }
    return null
  }

  async function submit(): Promise<void> {
    error.value = null
    copied.value = false
    analytics.value = null
    const validationError = validate()
    if (validationError) {
      error.value = validationError
      return
    }
    loading.value = true
    try {
      result.value = await createShortUrl(inputUrl.value.trim())
    } catch (e) {
      result.value = null
      error.value =
        e && typeof e === 'object' && 'message' in e
          ? String((e as { message: unknown }).message)
          : 'Failed to create short URL.'
    } finally {
      loading.value = false
    }
  }

  async function loadAnalytics(code: string): Promise<void> {
    error.value = null
    try {
      analytics.value = await getAnalytics(code)
    } catch (e) {
      analytics.value = null
      error.value =
        e && typeof e === 'object' && 'message' in e
          ? String((e as { message: unknown }).message)
          : 'Failed to load analytics.'
    }
  }

  async function copyResult(): Promise<void> {
    if (!result.value) return
    const text = result.value.short_url
    try {
      await navigator.clipboard.writeText(text)
      copied.value = true
    } catch {
      copied.value = false
      error.value = 'Copy failed. Select the URL manually.'
    }
  }

  return {
    inputUrl,
    loading,
    result,
    analytics,
    error,
    copied,
    validate,
    submit,
    loadAnalytics,
    copyResult,
  }
}
