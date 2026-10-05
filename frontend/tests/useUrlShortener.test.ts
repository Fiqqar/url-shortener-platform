import { describe, expect, it, vi } from 'vitest'
import { isValidHttpUrl, useUrlShortener } from '../src/composables/useUrlShortener'

vi.mock('../src/services/api', () => ({
  createShortUrl: vi.fn(async (url: string) => ({
    code: 'abc123',
    short_url: 'http://localhost:8000/abc123',
    target_url: url,
  })),
  getAnalytics: vi.fn(async (code: string) => ({ code, clicks: 2 })),
}))

describe('useUrlShortener', () => {
  it('rejects empty input without calling api', async () => {
    const s = useUrlShortener()
    s.inputUrl.value = '   '
    await s.submit()
    expect(s.error.value).toContain('empty')
    expect(s.result.value).toBeNull()
  })

  it('rejects unsupported scheme', async () => {
    const s = useUrlShortener()
    s.inputUrl.value = 'ftp://example.com/file'
    await s.submit()
    expect(s.error.value).toContain('http')
  })

  it('creates short url and loads analytics', async () => {
    const s = useUrlShortener()
    s.inputUrl.value = 'https://example.com/hello'
    await s.submit()
    expect(s.loading.value).toBe(false)
    expect(s.result.value?.code).toBe('abc123')
    await s.loadAnalytics('abc123')
    expect(s.analytics.value?.clicks).toBe(2)
  })

  it('validates http urls', () => {
    expect(isValidHttpUrl('https://example.com')).toBe(true)
    expect(isValidHttpUrl('http://localhost:8000/x')).toBe(true)
    expect(isValidHttpUrl('ftp://example.com')).toBe(false)
    expect(isValidHttpUrl('not a url')).toBe(false)
  })
})
