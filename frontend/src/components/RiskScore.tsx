export function RiskScore({ score, level }: { score: number; level: string }) {
  return (
    <section className="result-panel">
      <div className="risk-score-label">RISK SCORE</div>
      <div className="risk-score-value">{score}/100</div>
      <div className="risk-score-level">{level}</div>
    </section>
  )
}
