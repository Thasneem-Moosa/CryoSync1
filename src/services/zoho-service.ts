import { apiClient } from './api'

export interface ZohoSyncParams {
  /** Re-pull every record instead of using the Modified_Time watermark. */
  full?: boolean
  /** Limit the sync to specific Zoho modules (defaults to all available modules). */
  modules?: string[]
}

export interface ZohoSyncSummary {
  synced_at: string
  duration_s: number
  modules: number
  records: number
  per_module: Array<{ module: string; records: number }>
  failed: Array<{ module: string; error: string }>
}

/** Trigger an on-demand Zoho CRM → Databricks bronze sync. */
export async function syncZohoCrm(params?: ZohoSyncParams): Promise<ZohoSyncSummary> {
  return apiClient.post<ZohoSyncSummary>('/admin/sync-zoho', params ?? {})
}
