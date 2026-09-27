import type { EvidenceItem } from '../types/investigation'

export function Explanation({ evidence }: { evidence: EvidenceItem[] }) {
  return (
    <section className="result-panel">
      <h3>Why was this flagged?</h3>
      <div className="explanation-list">
        {evidence.map((item, index) => (
          <div className={`explanation-item severity-${item.severity}`} key={index}>
            <div className="explanation-header">
              <span className="explanation-indicator">{item.type}</span>
              <span className="explanation-severity">{item.severity.toUpperCase()}</span>
            </div>
            <span className="explanation-reason">{item.reason}</span>
          </div>
        ))}
      </div>
    </section>
  )
}
