export function Explanation({ evidence }: { evidence: Array<{ indicator: string; severity: string; reason: string }> }) {
  return (
    <section className="result-panel">
      <h3>Why was this flagged?</h3>
      <div className="explanation-list">
        {evidence.map((item, index) => (
          <div className="explanation-item" key={index}>
            <span className="explanation-indicator">{item.indicator}</span>
            <span className="explanation-reason">{item.reason}</span>
          </div>
        ))}
      </div>
    </section>
  )
}
