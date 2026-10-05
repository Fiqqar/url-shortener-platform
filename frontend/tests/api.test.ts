import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createShortUrl, getAnalytics } from '../src/services/api'

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

describe('api service', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('parses successful create response', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        jsonResponse({
          code: 'abc123',
          short_url: 'http://localhost:8000/abc123',
          target_url: 'https://example.com/x',
        }),
      ),
    )
    const res = await createShortUrl('https://example.com/x')
    expect(res.code).toBe('abc123')
    expect(res.short_url).toContain('/abc123')
  })

  it('maps 400 to validation error', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => jsonResponse({ detail: 'Could not create' }, 400)),
    )
    await expect(createShortUrl('ftp://bad')).rejects.toMatchObject({
      kind: 'validation',
    })
  })

  it('maps 404 analytics to not-found', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => jsonResponse({ detail: 'missing' }, 404)),
    )
    await expect(getAnalytics('ZZZ999nope')).rejects.toMatchObject({
      kind: 'not-found',
    })
  })

  it('maps network failure to network error', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => {
        throw new Error('down')
      }),
    )
    await expect(createShortUrl('https://example.com/x')).rejects.toMatchObject({
      kind: 'network',
    })
  })
})
