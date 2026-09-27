export function ScamType({ scamType }: { scamType: string }) {
  return (
    <section className="result-panel">
      <div className="result-label">Scam Type</div>
      <div className="result-value">{scamType}</div>
    </section>
  )
}
