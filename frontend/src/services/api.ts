// API Service client for AgroVision-Mine
import type {
  OverviewResponse,
  DatasetResponse,
  SpecimenDetail,
  WarehouseSchemaResponse,
  OLAPMetadataResponse,
  OLAPQueryResponse,
  ClusteringResponse,
  AssociationRulesResponse,
  HealthResponse,
  ImageAnalysisResponse,
} from '../types/api'

const API_BASE = '/api'

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, options)
  if (!res.ok) {
    const errorText = await res.text()
    throw new Error(`API Error ${res.status}: ${errorText}`)
  }
  return res.json()
}

export const api = {
  getHealth: () => fetchJson<HealthResponse>(`${API_BASE}/health`),

  getOverview: () => fetchJson<OverviewResponse>(`${API_BASE}/overview`),

  getDataset: (params: {
    page?: number
    page_size?: number
    crop?: string
    condition?: string
    pathogen?: string
    pest?: string
    source?: string
    search?: string
    sort_by?: string
    sort_order?: string
  }) => {
    const query = new URLSearchParams()
    if (params.page) query.set('page', params.page.toString())
    if (params.page_size) query.set('page_size', params.page_size.toString())
    if (params.crop) query.set('crop', params.crop)
    if (params.condition) query.set('condition', params.condition)
    if (params.pathogen) query.set('pathogen', params.pathogen)
    if (params.pest) query.set('pest', params.pest)
    if (params.source) query.set('source', params.source)
    if (params.search) query.set('search', params.search)
    if (params.sort_by) query.set('sort_by', params.sort_by)
    if (params.sort_order) query.set('sort_order', params.sort_order)
    return fetchJson<DatasetResponse>(`${API_BASE}/dataset?${query.toString()}`)
  },

  getSpecimenDetail: (imageId: string) =>
    fetchJson<SpecimenDetail>(`${API_BASE}/dataset/${encodeURIComponent(imageId)}`),

  getDataQuality: () => fetchJson<any>(`${API_BASE}/data-quality`),

  getWarehouseSchema: () =>
    fetchJson<WarehouseSchemaResponse>(`${API_BASE}/warehouse/schema`),

  getOLAPMetadata: () => fetchJson<OLAPMetadataResponse>(`${API_BASE}/olap/metadata`),

  executeOLAPQuery: (body: {
    operation: string
    crop_category?: string
    pathogen_type?: string
    crop_name?: string
    selected_crops?: string[]
    selected_pathogens?: string[]
    min_contrast?: number
    pivot_measure?: string
  }) =>
    fetchJson<OLAPQueryResponse>(`${API_BASE}/olap/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }),

  getClusteringResults: (selectedK: number = 2, maxPoints: number = 2596) =>
    fetchJson<ClusteringResponse>(
      `${API_BASE}/mining/clustering?selected_k=${selectedK}&max_points=${maxPoints}`
    ),

  getAssociationRules: (params: {
    mode?: string
    min_support?: number
    min_confidence?: number
    min_lift?: number
    search?: string
    sort_by?: string
    sort_order?: string
    page?: number
    page_size?: number
  }) => {
    const query = new URLSearchParams()
    if (params.mode) query.set('mode', params.mode)
    if (params.min_support !== undefined) query.set('min_support', params.min_support.toString())
    if (params.min_confidence !== undefined) query.set('min_confidence', params.min_confidence.toString())
    if (params.min_lift !== undefined) query.set('min_lift', params.min_lift.toString())
    if (params.search) query.set('search', params.search)
    if (params.sort_by) query.set('sort_by', params.sort_by)
    if (params.sort_order) query.set('sort_order', params.sort_order)
    if (params.page) query.set('page', params.page.toString())
    if (params.page_size) query.set('page_size', params.page_size.toString())
    return fetchJson<AssociationRulesResponse>(`${API_BASE}/mining/association-rules?${query.toString()}`)
  },

  getReportsCatalog: () => fetchJson<any>(`${API_BASE}/reports`),

  getReportContent: (reportId: string) =>
    fetchJson<any>(`${API_BASE}/reports/${encodeURIComponent(reportId)}`),

  analyzeImage: async (file: File): Promise<ImageAnalysisResponse> => {
    const formData = new FormData()
    formData.append('file', file)
    const res = await fetch(`${API_BASE}/analyze/image`, {
      method: 'POST',
      body: formData,
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: `Upload failed (${res.status})` }))
      throw new Error(err.detail || `Upload failed (${res.status})`)
    }
    return res.json()
  },
}
