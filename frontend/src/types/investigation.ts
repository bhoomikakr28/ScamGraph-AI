export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'

export interface InvestigationRequest {
  text: string
}

export interface EvidenceItem {
  type: string
  severity: string
  reason: string
  source: string
}

export interface InvestigationResult {
  investigation_id: string
  risk_score: number
  risk_level: RiskLevel
  scam_probability: number
  scam_type: string
  indicators: string[]
  entities: {
    phone_numbers: string[]
    upi_ids: string[]
    urls: string[]
    emails: string[]
  }
  evidence: EvidenceItem[]
  recommendations: string[]
  timestamp: string
}

export interface InvestigationHistoryItem extends InvestigationResult {
  input_text?: string
}
