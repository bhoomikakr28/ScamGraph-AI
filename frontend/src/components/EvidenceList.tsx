import type { EvidenceItem } from '../types/investigation'

export function EvidenceList({ evidence }: { evidence: EvidenceItem[] }) {
  return (
    <section className="result-panel">
      <h3>Detected Indicators</h3>
      <ul className="evidence-list">
        {evidence.map((item, index) => (
          <li key={index}><span className="checkmark">✓</span> {item.type}</li>
        ))}
      </ul>
    </section>
  )
}
