import type { InvestigationResult } from '../types/investigation'

export function EntitiesSummary({ entities }: { entities: InvestigationResult['entities'] }) {
  const rows: Array<{ label: string; count: number }> = [
    { label: 'URLs', count: entities.urls?.length ?? 0 },
    { label: 'Phone Numbers', count: entities.phone_numbers?.length ?? 0 },
    { label: 'UPI IDs', count: entities.upi_ids?.length ?? 0 },
    { label: 'Emails', count: entities.emails?.length ?? 0 },
  ]

  return (
    <section className="result-panel">
      <h3>Extracted Entities</h3>
      <div className="entities-grid">
        {rows.map((row) => (
          <div className="entity-cell" key={row.label}>
            <span className="entity-label">{row.label}</span>
            <span className="entity-count">{row.count}</span>
          </div>
        ))}
      </div>
    </section>
  )
}
