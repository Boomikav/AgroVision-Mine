import React, { useEffect, useState } from 'react'
import { api } from '../../services/api'
import type { SpecimenDetail } from '../../types/api'

interface SpecimenModalProps {
  imageId: string | null
  onClose: () => void
}

export const SpecimenModal: React.FC<SpecimenModalProps> = ({ imageId, onClose }) => {
  const [detail, setDetail] = useState<SpecimenDetail | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'all' | 'color' | 'texture' | 'shape'>('all')

  useEffect(() => {
    if (!imageId) return
    setLoading(true)
    setError(null)
    api
      .getSpecimenDetail(imageId)
      .then((data) => {
        setDetail(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [imageId])

  if (!imageId) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fadeIn">
      <div className="bg-[#FFFFFF] rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col border border-[#E2E7DF] shadow-2xl">
        {/* Header */}
        <div className="px-6 py-4 bg-[#24342D] text-white flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-[#34765B] flex items-center justify-center">
              <span className="material-symbols-outlined text-[18px]">biotech</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-headline font-semibold text-base sm:text-lg">
                  Specimen Inspector: {imageId}
                </span>
                {detail && (
                  <span
                    className={`px-2 py-0.5 rounded font-mono text-[10px] font-bold uppercase ${
                      detail.condition_label?.toLowerCase() === 'healthy'
                        ? 'bg-[#C3EFAA] text-[#2B4F1C]'
                        : 'bg-[#FFDAD6] text-[#93000A]'
                    }`}
                  >
                    {detail.condition_label}
                  </span>
                )}
              </div>
              <p className="font-mono text-xs text-[#E2F5EB]/70">
                {detail?.filename || 'Loading manifest record...'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition-colors"
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto flex-1 flex flex-col gap-6">
          {loading && (
            <div className="flex flex-col items-center justify-center py-16 gap-3 text-[#404943]">
              <span className="material-symbols-outlined text-4xl animate-spin text-[#175D44]">
                progress_activity
              </span>
              <span className="text-sm">Retrieving specimen feature tensor...</span>
            </div>
          )}

          {error && (
            <div className="p-4 rounded-xl bg-[#FFDAD6] text-[#93000A] text-sm flex items-center gap-2">
              <span className="material-symbols-outlined">error</span>
              <span>{error}</span>
            </div>
          )}

          {!loading && detail && (
            <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
              {/* Left Column: Image raster + Core attributes */}
              <div className="md:col-span-5 flex flex-col gap-4">
                <div className="relative aspect-square w-full rounded-xl overflow-hidden bg-[#E5F8ED] border border-[#E2E7DF] flex items-center justify-center shadow-inner">
                  <img
                    src={detail.image_url}
                    alt={detail.image_id}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      // Fallback to SVG if image fails to render
                      ;(e.target as HTMLImageElement).src = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300"><rect width="300" height="300" fill="%23E5F8ED"/><text x="150" y="150" font-family="sans-serif" font-size="14" fill="%2326362F" text-anchor="middle">Raster Archived</text></svg>`
                    }}
                  />
                  <span className="absolute bottom-2 left-2 px-2 py-0.5 rounded bg-black/60 text-white font-mono text-[10px] backdrop-blur-sm">
                    {detail.dominant_color_tone}
                  </span>
                </div>

                <div className="p-4 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2.5 text-xs">
                  <div className="flex justify-between items-center">
                    <span className="text-[#404943]">Crop Taxon:</span>
                    <span className="font-semibold text-[#0F1F18]">{detail.crop_label}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-[#404943]">Pathology / Disease:</span>
                    <span className="font-semibold text-[#0F1F18]">{detail.disease_label}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-[#404943]">Pathogen Etiology:</span>
                    <span className="font-mono text-[#0F1F18]">{detail.pathogen_type}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-[#404943]">Pest Symptoms:</span>
                    <span className="font-mono">{detail.is_pest ? 'Present' : 'Absent'}</span>
                  </div>
                  <div className="h-px bg-[#E2E7DF] my-1" />
                  <div className="flex justify-between items-center">
                    <span className="text-[#404943]">K=2 Cluster:</span>
                    <span className="px-2 py-0.5 rounded font-mono text-[11px] bg-[#E0F2E8] text-[#175D44] font-bold">
                      Cluster {detail.cluster_id_k2}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-[#404943]">K=4 Sub-partition:</span>
                    <span className="px-2 py-0.5 rounded font-mono text-[11px] bg-[#E0F2E8] text-[#175D44] font-bold">
                      Cluster {detail.cluster_id_k4}
                    </span>
                  </div>
                  {detail.pca_coordinates.x !== null && (
                    <div className="flex justify-between items-center">
                      <span className="text-[#404943]">PCA Projection (PC1, PC2):</span>
                      <span className="font-mono text-[#0F1F18]">
                        ({detail.pca_coordinates.x}, {detail.pca_coordinates.y})
                      </span>
                    </div>
                  )}
                </div>
              </div>

              {/* Right Column: 32 Continuous Visual Features Vector */}
              <div className="md:col-span-7 flex flex-col gap-3">
                <div className="flex items-center justify-between">
                  <h3 className="font-headline font-semibold text-sm text-[#0F1F18]">
                    Extracted Visual Feature Tensor (32 Vectors)
                  </h3>
                  <div className="flex p-0.5 rounded-lg bg-[#E0F2E8] text-xs">
                    {(['all', 'color', 'texture', 'shape'] as const).map((t) => (
                      <button
                        key={t}
                        onClick={() => setActiveTab(t)}
                        className={`px-2.5 py-1 rounded capitalize font-medium transition-all ${
                          activeTab === t
                            ? 'bg-[#175D44] text-white shadow-xs'
                            : 'text-[#404943] hover:text-[#0F1F18]'
                        }`}
                      >
                        {t}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="border border-[#E2E7DF] rounded-xl overflow-hidden bg-white max-h-96 overflow-y-auto">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead className="bg-[#E5F8ED] text-[#175D44] font-mono text-[11px] sticky top-0">
                      <tr>
                        <th className="py-2 px-3 font-semibold">Descriptor Token</th>
                        <th className="py-2 px-3 font-semibold">Domain</th>
                        <th className="py-2 px-3 text-right font-semibold">Value</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#E2E7DF]">
                      {Object.entries({
                        ...(activeTab === 'all' || activeTab === 'color' ? detail.color_features : {}),
                        ...(activeTab === 'all' || activeTab === 'texture' ? detail.glcm_features : {}),
                        ...(activeTab === 'all' || activeTab === 'shape' ? detail.shape_features : {}),
                      }).map(([k, v]) => {
                        const domain = k.startsWith('rgb') || k.startsWith('hsv') || k.startsWith('exg')
                          ? 'Color'
                          : k.startsWith('glcm')
                          ? 'GLCM Texture'
                          : 'Contour/Shape'
                        return (
                          <tr key={k} className="hover:bg-[#F7F6EF] transition-colors">
                            <td className="py-2 px-3 font-mono font-medium text-[#0F1F18]">{k}</td>
                            <td className="py-2 px-3 text-[#404943]">{domain}</td>
                            <td className="py-2 px-3 text-right font-mono text-[#175D44] font-semibold">
                              {typeof v === 'number' ? v.toFixed(4) : v}
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>

                <div className="p-3 rounded-lg bg-[#E0F2E8]/60 text-[11px] text-[#404943] flex items-center gap-2">
                  <span className="material-symbols-outlined text-[16px] text-[#175D44]">
                    verified
                  </span>
                  <span>
                    Features standardized via z-score normalization across all 2,596 canonical specimens.
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
