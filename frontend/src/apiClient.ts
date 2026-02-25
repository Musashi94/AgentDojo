const API_BASE_URL = import.meta.env.API_BASE_URL || import.meta.env.VITE_API_BASE_URL || ''

export type PingResponse = {
  ok?: boolean
  message?: string
  [key: string]: unknown
}

export async function pingV03(signal?: AbortSignal): Promise<PingResponse> {
  const base = API_BASE_URL.replace(/\/$/, '')
  const response = await fetch(`${base}/v03/ping`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
    signal,
  })

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  const contentType = response.headers.get('content-type') ?? ''
  if (contentType.includes('application/json')) {
    return (await response.json()) as PingResponse
  }

  const text = await response.text()
  return { message: text }
}
