import { useEffect, useState } from 'react'
import { pingV03, type PingResponse } from './apiClient'

type State = 'loading' | 'error' | 'success'

export function V03Dashboard() {
  const [state, setState] = useState<State>('loading')
  const [data, setData] = useState<PingResponse | null>(null)
  const [error, setError] = useState<string>('')

  useEffect(() => {
    const controller = new AbortController()

    pingV03(controller.signal)
      .then((result) => {
        setData(result)
        setState('success')
      })
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === 'AbortError') {
          return
        }

        setError(err instanceof Error ? err.message : 'Unknown error')
        setState('error')
      })

    return () => controller.abort()
  }, [])

  return (
    <main style={{ maxWidth: 720, margin: '4rem auto', padding: '0 1rem', fontFamily: 'Inter, system-ui, sans-serif' }}>
      <h1>Frontend v0.3</h1>
      <h2>V03Dashboard</h2>

      {state === 'loading' && <p>Loading /v03/ping …</p>}

      {state === 'error' && (
        <div>
          <p>Request failed.</p>
          <pre>{error}</pre>
        </div>
      )}

      {state === 'success' && (
        <div>
          <p>Ping successful.</p>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </main>
  )
}
