export function MessageInput({ value, onChange, onAnalyze }: { value: string; onChange: (value: string) => void; onAnalyze: () => void }) {
  return (
    <div className="message-input-card">
      <textarea value={value} onChange={(event) => onChange(event.target.value)} placeholder="Paste a suspicious message here..." rows={7} />
      <button className="analyze-button" onClick={onAnalyze}>ANALYZE MESSAGE</button>
    </div>
  )
}
