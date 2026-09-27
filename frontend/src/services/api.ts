const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

export async function analyzeMessage(text: string) {
  const response = await fetch(`${API_BASE}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Analysis failed.' }))
    throw new Error(error.detail ?? 'Analysis failed.')
  }

  return response.json()
}

export async function getInvestigations() {
  const response = await fetch(`${API_BASE}/api/investigations`)
  if (!response.ok) {
    throw new Error('Unable to load investigation history.')
  }
  return response.json()
}
