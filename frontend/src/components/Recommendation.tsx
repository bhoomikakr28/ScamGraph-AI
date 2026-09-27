export function Recommendation({ recommendations }: { recommendations: string[] }) {
  return (
    <section className="result-panel">
      <h3>Recommended Action</h3>
      <ul className="recommendation-list">
        {recommendations.map((recommendation, index) => (
          <li key={index}>{recommendation}</li>
        ))}
      </ul>
    </section>
  )
}
