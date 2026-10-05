import type {
  AnalyticsResponse,
  ApiError,
  CreateUrlResponse,
  UrlInfoResponse,
} from '../types/api'

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') ||
  'http://localhost:8000'

function toApiError(status: number, detail: unknown): ApiError {
  const message =
    typeof detail === 'string'
      ? detail
      : 'Request failed. Please try again.'
  if (status === 400 || status === 422) {
    return { kind: 'validation', message, status }
  }
  if (status === 404) {
    return { kind: 'not-found', message: 'Short URL not found.', status }
  }
  if (status === 503) {
    return { kind: 'server', message: 'Storage unavailable. Try again later.', status }
  }
  return { kind: 'server', message, status }
}

async function parseJsonSafe(res: Response): Promise<unknown> {
  try {
    return await res.json()
  } catch {
    return null
  }
}

export async function createShortUrl(targetUrl: string): Promise<CreateUrlResponse> {
  let res: Response
  try {
    res = await fetch(`${BASE_URL}/api/v1/urls`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: targetUrl }),
    })
  } catch {
    throw { kind: 'network', message: 'Cannot reach backend. Is it running?' } satisfies ApiError
  }
  if (!res.ok) {
    const body = await parseJsonSafe(res)
    const detail =
      body && typeof body === 'object' && 'detail' in body
        ? String((body as { detail: unknown }).detail)
        : `Request failed with status ${res.status}`
    throw toApiError(res.status, detail)
  }
  return (await res.json()) as CreateUrlResponse
}

export async function getUrlInfo(code: string): Promise<UrlInfoResponse> {
  let res: Response
  try {
    res = await fetch(`${BASE_URL}/api/v1/urls/${encodeURIComponent(code)}`)
  } catch {
    throw { kind: 'network', message: 'Cannot reach backend. Is it running?' } satisfies ApiError
  }
  if (!res.ok) {
    throw toApiError(res.status, 'Short URL not found.')
  }
  return (await res.json()) as UrlInfoResponse
}

export async function getAnalytics(code: string): Promise<AnalyticsResponse> {
  let res: Response
  try {
    res = await fetch(
      `${BASE_URL}/api/v1/urls/${encodeURIComponent(code)}/analytics`,
    )
  } catch {
    throw { kind: 'network', message: 'Cannot reach backend. Is it running?' } satisfies ApiError
  }
  if (!res.ok) {
    throw toApiError(res.status, 'Short URL not found.')
  }
  return (await res.json()) as AnalyticsResponse
}

export function getBaseUrl(): string {
  return BASE_URL
}
