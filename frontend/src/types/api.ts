export interface CreateUrlRequest {
  url: string
}

export interface CreateUrlResponse {
  code: string
  short_url: string
  target_url: string
}

export interface UrlInfoResponse {
  code: string
  short_url: string
  target_url: string
  clicks: number
}

export interface AnalyticsResponse {
  code: string
  clicks: number
}

export type ApiErrorKind =
  | 'validation'
  | 'not-found'
  | 'server'
  | 'network'

export interface ApiError {
  kind: ApiErrorKind
  message: string
  status?: number
}
