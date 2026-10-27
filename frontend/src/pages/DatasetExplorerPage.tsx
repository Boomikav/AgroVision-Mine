import React, { useEffect, useState } from 'react'
import { api } from '../services/api'
import type { DatasetResponse } from '../types/api'
import { SpecimenModal } from '../components/common/SpecimenModal'
import { AppIcon } from '../components/common/AppIcon'

interface DatasetExplorerPageProps {
  initialSearch?: string
}

export const DatasetExplorerPage: React.FC<DatasetExplorerPageProps> = ({ initialSearch = '' }) => {
  const [data, setData] = useState<DatasetResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedImageId, setSelectedImageId] = useState<string | null>(null)

  // Filters state
  const [search, setSearch] = useState(initialSearch)
  const [crop, setCrop] = useState<string>('all')
  const [condition, setCondition] = useState<string>('all')
  const [pathogen, setPathogen] = useState<string>('all')
  const [pest, setPest] = useState<string>('all')
  const [source, setSource] = useState<string>('all')
  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(24)
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid')
  const [sortBy] = useState<string>('image_id')
  const [sortOrder] = useState<string>('asc')

  const fetchDataset = () => {
    setLoading(true)
    api
      .getDataset({
        page,
        page_size: pageSize,
        crop: crop !== 'all' ? crop : undefined,
        condition: condition !== 'all' ? condition : undefined,
        pathogen: pathogen !== 'all' ? pathogen : undefined,
        pest: pest !== 'all' ? pest : undefined,
        source: source !== 'all' ? source : undefined,
        search: search.trim() ? search.trim() : undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
      })
      .then((res) => {
        setData(res)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load dataset records:', err)
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchDataset()
  }, [page, pageSize, crop, condition, pathogen, pest, source, sortBy, sortOrder])

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setPage(1)
    fetchDataset()
  }

  const handleResetFilters = () => {
    setSearch('')
    setCrop('all')
    setCondition('all')
    setPathogen('all')
    setPest('all')
    setSource('all')
    setPage(1)
  }

  const activeFiltersCount =
    (crop !== 'all' ? 1 : 0) +
    (condition !== 'all' ? 1 : 0) +
    (pathogen !== 'all' ? 1 : 0) +
    (pest !== 'all' ? 1 : 0) +
    (source !== 'all' ? 1 : 0) +
    (search.trim() ? 1 : 0)

  const handleExportCsv = () => {
    if (!data?.records.length) return
    const headers = [
      'image_id',
      'crop_name',
      'disease_name',
      'condition_status',
      'pathogen_type',
      'dominant_color_tone',
      'cluster_id_k2',
      'cluster_id_k4',
      'dataset_source',
    ]
    const rows = data.records.map((r) => [
      r.image_id,
      r.crop_name,
      r.disease_name,
      r.condition_status,
      r.pathogen_type,
      r.dominant_color_tone,
      r.cluster_id_k2 ?? '',
      r.cluster_id_k4 ?? '',
      r.dataset_source,
    ])
    const csvContent =
      'data:text/csv;charset=utf-8,' +
      [headers.join(','), ...rows.map((e) => e.join(','))].join('\n')
    const encodedUri = encodeURI(csvContent)
    const link = document.createElement('a')
    link.setAttribute('href', encodedUri)
    link.setAttribute('download', `agrovision_dataset_page_${page}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="flex flex-col gap-6 max-w-[1720px] mx-auto w-full pb-12">
      {/* Top Filter and Search Control Bar */}
      <section className="bg-white rounded-2xl p-5 border border-[#E2E7DF] shadow-xs flex flex-col gap-4">
        {/* Row 1: Search & Controls */}
        <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4">
          <form onSubmit={handleSearchSubmit} className="relative flex-1 max-w-xl">
            <AppIcon name="search" className="absolute left-3 top-1/2 -translate-y-1/2 text-[#707973] text-[20px]" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by Image ID (e.g. AGRO_V2_00001), Crop, Disease..."
              className="w-full pl-10 pr-20 py-2 rounded-xl bg-[#F7F6EF] border border-[#BFC9C2]/40 text-xs text-[#0F1F18] placeholder:text-[#404943]/60 focus:outline-none focus:bg-white focus:border-[#175D44] transition-all"
            />
            {search && (
              <button
                type="button"
                onClick={() => {
                  setSearch('')
                  setPage(1)
                }}
                className="absolute right-12 top-1/2 -translate-y-1/2 text-[#707973] hover:text-[#0F1F18]"
              >
                <AppIcon name="close" className="text-[16px]" />
              </button>
            )}
            <button
              type="submit"
              className="absolute right-2 top-1/2 -translate-y-1/2 px-2 py-0.5 rounded bg-[#175D44] text-white font-mono text-[10px] font-semibold"
            >
              FIND
            </button>
          </form>

          <div className="flex items-center gap-3 self-end lg:self-auto">
            {/* Active records count */}
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#E0F2E8] font-mono text-xs text-[#175D44]">
              <span className="w-2 h-2 rounded-full bg-[#175D44]" />
              <span>
                Records: <strong>{data?.total_records.toLocaleString() ?? '...'}</strong> of{' '}
                <strong>2,596</strong>
              </span>
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center p-1 rounded-lg bg-[#F7F6EF] border border-[#E2E7DF]">
              <button
                onClick={() => setViewMode('grid')}
                className={`flex items-center gap-1 px-3 py-1.5 rounded text-xs transition-all ${
                  viewMode === 'grid'
                    ? 'bg-white text-[#175D44] font-semibold shadow-xs'
                    : 'text-[#404943] hover:text-[#0F1F18]'
                }`}
              >
                <AppIcon name="grid_view" className="text-[16px]" />
                <span className="hidden md:inline">Grid</span>
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`flex items-center gap-1 px-3 py-1.5 rounded text-xs transition-all ${
                  viewMode === 'table'
                    ? 'bg-white text-[#175D44] font-semibold shadow-xs'
                    : 'text-[#404943] hover:text-[#0F1F18]'
                }`}
              >
                <AppIcon name="table_rows" className="text-[16px]" />
                <span className="hidden md:inline">Table</span>
              </button>
            </div>

            {/* Export CSV */}
            <button
              onClick={handleExportCsv}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#34765B] text-white hover:bg-[#175D44] text-xs font-semibold transition-colors shadow-xs"
            >
              <AppIcon name="file_download" className="text-[16px]" />
              <span>Export CSV</span>
            </button>
          </div>
        </div>

        {/* Row 2: Slicers */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 pt-2 border-t border-[#E2E7DF]">
          {/* Crop Slicer */}
          <div className="flex flex-col gap-1">
            <label className="font-mono text-[10px] uppercase tracking-wider text-[#404943] font-medium">
              Crop Taxon
            </label>
            <select
              value={crop}
              onChange={(e) => {
                setCrop(e.target.value)
                setPage(1)
              }}
              className="w-full px-2.5 py-1.5 rounded-lg bg-[#F7F6EF] text-xs text-[#0F1F18] border border-[#BFC9C2]/40 focus:outline-none focus:border-[#175D44]"
            >
              <option value="all">All 14 Crops</option>
              {data?.filter_options.crops.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          {/* Condition Slicer */}
          <div className="flex flex-col gap-1">
            <label className="font-mono text-[10px] uppercase tracking-wider text-[#404943] font-medium">
              Condition
            </label>
            <select
              value={condition}
              onChange={(e) => {
                setCondition(e.target.value)
                setPage(1)
              }}
              className="w-full px-2.5 py-1.5 rounded-lg bg-[#F7F6EF] text-xs text-[#0F1F18] border border-[#BFC9C2]/40 focus:outline-none focus:border-[#175D44]"
            >
              <option value="all">All Conditions</option>
              <option value="Diseased">Diseased (Pathological)</option>
              <option value="Healthy">Healthy (Baseline)</option>
            </select>
          </div>

          {/* Pathogen Slicer */}
          <div className="flex flex-col gap-1">
            <label className="font-mono text-[10px] uppercase tracking-wider text-[#404943] font-medium">
              Pathogen Type
            </label>
            <select
              value={pathogen}
              onChange={(e) => {
                setPathogen(e.target.value)
                setPage(1)
              }}
              className="w-full px-2.5 py-1.5 rounded-lg bg-[#F7F6EF] text-xs text-[#0F1F18] border border-[#BFC9C2]/40 focus:outline-none focus:border-[#175D44]"
            >
              <option value="all">All Pathogens</option>
              {data?.filter_options.pathogens.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </div>

          {/* Pest Slicer */}
          <div className="flex flex-col gap-1">
            <label className="font-mono text-[10px] uppercase tracking-wider text-[#404943] font-medium">
              Pest Symptoms
            </label>
            <select
              value={pest}
              onChange={(e) => {
                setPest(e.target.value)
                setPage(1)
              }}
              className="w-full px-2.5 py-1.5 rounded-lg bg-[#F7F6EF] text-xs text-[#0F1F18] border border-[#BFC9C2]/40 focus:outline-none focus:border-[#175D44]"
            >
              <option value="all">All Signs</option>
              <option value="yes">Present</option>
              <option value="no">Absent</option>
            </select>
          </div>

          {/* Archive Source */}
          <div className="flex flex-col gap-1">
            <label className="font-mono text-[10px] uppercase tracking-wider text-[#404943] font-medium">
              Source Archive
            </label>
            <select
              value={source}
              onChange={(e) => {
                setSource(e.target.value)
                setPage(1)
              }}
              className="w-full px-2.5 py-1.5 rounded-lg bg-[#F7F6EF] text-xs text-[#0F1F18] border border-[#BFC9C2]/40 focus:outline-none focus:border-[#175D44]"
            >
              <option value="all">All Sources</option>
              <option value="plantdoc">PlantDoc (2,560)</option>
              <option value="icar_ogd">ICAR / OGD (36)</option>
            </select>
          </div>

          {/* Reset Filters */}
          <div className="flex items-end">
            <button
              onClick={handleResetFilters}
              disabled={activeFiltersCount === 0}
              className={`w-full flex items-center justify-center gap-1.5 py-1.5 rounded-lg text-xs transition-colors border ${
                activeFiltersCount > 0
                  ? 'bg-[#FFDAD6]/50 text-[#93000A] border-[#FFDAD6] hover:bg-[#FFDAD6]'
                  : 'bg-[#F7F6EF] text-[#707973] border-[#E2E7DF] cursor-not-allowed'
              }`}
            >
              <AppIcon name="restart_alt" className="text-[15px]" />
              <span>Reset ({activeFiltersCount})</span>
            </button>
          </div>
        </div>
      </section>

      {/* Main Specimen Grid / Table View */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 gap-3 text-[#404943]">
          <AppIcon name="progress_activity" className="text-4xl animate-spin text-[#175D44]" />
          <span className="text-sm font-mono">Retrieving specimen inventory from data warehouse...</span>
        </div>
      ) : data?.records.length === 0 ? (
        <div className="bg-white rounded-2xl p-12 text-center border border-[#E2E7DF] flex flex-col items-center gap-3">
          <AppIcon name="search_off" className="text-4xl text-[#707973]" />
          <h3 className="font-headline font-semibold text-lg text-[#0F1F18]">
            No matching specimens found
          </h3>
          <p className="text-xs text-[#404943] max-w-md">
            No records match the current filter selection. Try resetting filters or using a broader query.
          </p>
          <button
            onClick={handleResetFilters}
            className="px-4 py-2 rounded-lg bg-[#175D44] text-white text-xs font-semibold"
          >
            Reset Filters
          </button>
        </div>
      ) : viewMode === 'grid' ? (
        /* GRID VIEW */
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {data?.records.map((rec) => {
            const isHealthy = rec.condition_status.toLowerCase() === 'healthy'
            return (
              <div
                key={rec.image_id}
                onClick={() => setSelectedImageId(rec.image_id)}
                className="group bg-white rounded-xl overflow-hidden border border-[#E2E7DF] hover:border-[#175D44] shadow-xs hover:shadow-md transition-all cursor-pointer flex flex-col justify-between"
              >
                {/* Raster thumbnail */}
                <div className="relative aspect-square w-full bg-[#E5F8ED] overflow-hidden flex items-center justify-center">
                  <img
                    src={`/api/dataset/${rec.image_id}/image`}
                    alt={rec.image_id}
                    loading="lazy"
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    onError={(e) => {
                      ;(e.target as HTMLImageElement).src = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" fill="%23E5F8ED"/><text x="100" y="100" font-family="monospace" font-size="10" fill="%2326362F" text-anchor="middle">${rec.image_id}</text></svg>`
                    }}
                  />
                  {/* Condition Tag */}
                  <span
                    className={`absolute top-2 right-2 px-1.5 py-0.5 rounded font-mono text-[9px] font-bold uppercase shadow-xs ${
                      isHealthy
                        ? 'bg-[#C3EFAA] text-[#2B4F1C]'
                        : 'bg-[#FFDAD6] text-[#93000A]'
                    }`}
                  >
                    {isHealthy ? 'Healthy' : 'Diseased'}
                  </span>

                  {/* Cluster indicator */}
                  {rec.cluster_id_k2 !== null && (
                    <span className="absolute bottom-2 left-2 px-1.5 py-0.5 rounded bg-black/60 text-white font-mono text-[9px] backdrop-blur-sm">
                      K2: C{rec.cluster_id_k2}
                    </span>
                  )}
                </div>

                {/* Card Details */}
                <div className="p-3 flex flex-col gap-1">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[11px] font-bold text-[#0F1F18] truncate">
                      {rec.image_id}
                    </span>
                    <span className="font-mono text-[9px] text-[#707973] uppercase">
                      {rec.dataset_source === 'plantdoc' ? 'PLANTDOC' : 'ICAR'}
                    </span>
                  </div>

                  <span className="text-xs font-semibold text-[#175D44] truncate">
                    {rec.crop_name}
                  </span>

                  <span className="text-[11px] text-[#404943] truncate">
                    {rec.disease_name}
                  </span>

                  <div className="mt-1 pt-1.5 border-t border-[#E2E7DF] flex items-center justify-between text-[10px] text-[#707973] font-mono">
                    <span className="truncate">{rec.dominant_color_tone}</span>
                    <span className="text-[#175D44] font-medium flex items-center gap-0.5">
                      Inspect
                      <AppIcon name="chevron_right" className="text-[12px]" />
                    </span>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        /* TABLE VIEW */
        <div className="bg-white rounded-2xl border border-[#E2E7DF] overflow-hidden shadow-xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead className="bg-[#E5F8ED] text-[#175D44] font-mono text-[11px] border-b border-[#E2E7DF]">
                <tr>
                  <th className="py-3 px-4 font-semibold">Image ID</th>
                  <th className="py-3 px-4 font-semibold">Crop</th>
                  <th className="py-3 px-4 font-semibold">Pathology / Disease</th>
                  <th className="py-3 px-4 font-semibold">Status</th>
                  <th className="py-3 px-4 font-semibold">Pathogen</th>
                  <th className="py-3 px-4 font-semibold">Dominant Tone</th>
                  <th className="py-3 px-4 font-semibold">K=2 Cluster</th>
                  <th className="py-3 px-4 font-semibold">PCA Coordinates</th>
                  <th className="py-3 px-4 font-semibold">Source</th>
                  <th className="py-3 px-4 text-right font-semibold">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E2E7DF]">
                {data?.records.map((rec) => {
                  const isHealthy = rec.condition_status.toLowerCase() === 'healthy'
                  return (
                    <tr
                      key={rec.image_id}
                      onClick={() => setSelectedImageId(rec.image_id)}
                      className="hover:bg-[#F7F6EF] transition-colors cursor-pointer"
                    >
                      <td className="py-2.5 px-4 font-mono font-bold text-[#0F1F18]">
                        {rec.image_id}
                      </td>
                      <td className="py-2.5 px-4 font-medium text-[#175D44]">{rec.crop_name}</td>
                      <td className="py-2.5 px-4 text-[#0F1F18]">{rec.disease_name}</td>
                      <td className="py-2.5 px-4">
                        <span
                          className={`px-2 py-0.5 rounded font-mono text-[10px] font-bold uppercase ${
                            isHealthy
                              ? 'bg-[#C3EFAA] text-[#2B4F1C]'
                              : 'bg-[#FFDAD6] text-[#93000A]'
                          }`}
                        >
                          {rec.condition_status}
                        </span>
                      </td>
                      <td className="py-2.5 px-4 text-[#404943]">{rec.pathogen_type}</td>
                      <td className="py-2.5 px-4 font-mono text-[11px] text-[#404943]">
                        {rec.dominant_color_tone}
                      </td>
                      <td className="py-2.5 px-4 font-mono text-[11px] font-semibold text-[#175D44]">
                        Cluster {rec.cluster_id_k2}
                      </td>
                      <td className="py-2.5 px-4 font-mono text-[11px] text-[#404943]">
                        {rec.pca_x !== null ? `(${rec.pca_x}, ${rec.pca_y})` : '—'}
                      </td>
                      <td className="py-2.5 px-4 font-mono text-[10px] text-[#707973] uppercase">
                        {rec.dataset_source}
                      </td>
                      <td className="py-2.5 px-4 text-right">
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            setSelectedImageId(rec.image_id)
                          }}
                          className="px-2.5 py-1 rounded bg-[#E0F2E8] text-[#175D44] font-medium hover:bg-[#175D44] hover:text-white transition-colors"
                        >
                          View
                        </button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Pagination Footer */}
      {data && data.total_pages > 1 && (
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 px-2 pt-2 text-xs text-[#404943]">
          <div className="flex items-center gap-2">
            <span>Rows per page:</span>
            <select
              value={pageSize}
              onChange={(e) => {
                setPageSize(Number(e.target.value))
                setPage(1)
              }}
              className="px-2 py-1 rounded bg-white border border-[#E2E7DF] font-mono text-xs"
            >
              <option value="12">12</option>
              <option value="24">24</option>
              <option value="48">48</option>
              <option value="96">96</option>
            </select>
            <span className="font-mono text-[#0F1F18]">
              Page {data.page} of {data.total_pages} ({data.total_records.toLocaleString()} total)
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="px-3 py-1.5 rounded-lg bg-white border border-[#E2E7DF] disabled:opacity-40 hover:bg-[#F7F6EF] transition-colors"
            >
              Previous
            </button>
            <span className="font-mono px-2 font-semibold text-[#175D44]">{page}</span>
            <button
              onClick={() => setPage((p) => Math.min(data.total_pages, p + 1))}
              disabled={page >= data.total_pages}
              className="px-3 py-1.5 rounded-lg bg-white border border-[#E2E7DF] disabled:opacity-40 hover:bg-[#F7F6EF] transition-colors"
            >
              Next
            </button>
          </div>
        </div>
      )}

      {/* Specimen Inspection Modal */}
      <SpecimenModal
        imageId={selectedImageId}
        onClose={() => setSelectedImageId(null)}
      />
    </div>
  )
}
