export function EvidenceList({ evidence }: { evidence: Array<{ indicator: string; severity: string; reason: string }> }) {
  return (
    <section className="result-panel">
      <h3>Detected Evidence</h3>
      <ul className="evidence-list">
        {evidence.map((item, index) => (
          <li key={index}><span className="checkmark">✓</span> {item.indicator}</li>
        ))}
      </ul>
    </section>
  )
}
