import { useState } from 'react'
import { analyzeMessage, getInvestigations } from '../services/api'
import { MessageInput } from '../components/MessageInput'
import { RiskScore } from '../components/RiskScore'
import { EvidenceList } from '../components/EvidenceList'
import { ScamType } from '../components/ScamType'
import { Explanation } from '../components/Explanation'
import { Recommendation } from '../components/Recommendation'
import { EntitiesSummary } from '../components/EntitiesSummary'
import type { InvestigationResult } from '../types/investigation'

export function Dashboard() {
  const [text, setText] = useState('')
  const [result, setResult] = useState<InvestigationResult | null>(null)
  const [history, setHistory] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyze = async () => {
    const value = text.trim()
    if (!value) {
      setError('Please enter a message before analyzing.')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await analyzeMessage(value)
      setResult(response)
      const investigations = await getInvestigations()
      setHistory(investigations)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <h1>SCAMGRAPH AI</h1>
          <p className="tagline">Don't just detect the scam. Understand the scam.</p>
        </div>
      </header>

      <main className="dashboard-grid">
        <section className="analysis-column">
          <MessageInput value={text} onChange={setText} onAnalyze={handleAnalyze} />

          <div className="example-messages">
            <button onClick={() => setText('Urgent bank alert: account will be blocked today. Verify your OTP immediately.')}>Bank alert example</button>
            <button onClick={() => setText('Congratulations! You have won a prize. Claim your reward through a secure link.')}>Lottery example</button>
          </div>

          {error && <div className="error-box">{error}</div>}
          {loading && <div className="loading-box">Analyzing...</div>}

          {result && (
            <section className="results">
              <RiskScore score={result.risk_score} level={result.risk_level} />
              <ScamType scamType={result.scam_type} />
              <div className="probability-row">
                <span>Scam Probability</span>
                <strong>{Math.round(result.scam_probability * 100)}%</strong>
              </div>
              <EvidenceList evidence={result.evidence} />
              <EntitiesSummary entities={result.entities} />
              <Explanation evidence={result.evidence} />
              <Recommendation recommendations={result.recommendations} />
            </section>
          )}
        </section>

        <aside className="history-column">
          <h2>Investigation History</h2>
          {history.length === 0 ? <p>No investigations yet.</p> : history.map((item) => (
            <button className="history-item" key={item.investigation_id} onClick={() => setResult(item)}>
              <span className="history-id">Investigation #{String(item.investigation_id).padStart(3, '0')}</span>
              <span className="history-level">{item.risk_level}</span>
              <span className="history-type">{item.scam_type}</span>
              <span className="history-score">{item.risk_score}/100</span>
            </button>
          ))}
        </aside>
      </main>
    </div>
  )
}
