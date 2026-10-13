import React, { useEffect, useState } from 'react'
import { api } from '../services/api'
import type { OLAPQueryResponse } from '../types/api'
import { SectionCard } from '../components/common/SectionCard'

export const OLAPAnalyticsPage: React.FC = () => {
  const [activeOp, setActiveOp] = useState<string>('rollup')
  const [queryResult, setQueryResult] = useState<OLAPQueryResponse | null>(null)
  const [loading, setLoading] = useState(false)

  // Operation parameters
  const [sliceCrop, setSliceCrop] = useState<string>('Rice')
  const [slicePathogen, setSlicePathogen] = useState<string>('Fungal')
  const [drilldownCategory, setDrilldownCategory] = useState<string>('Cereal')
  const [trueDrilldownPathogen, setTrueDrilldownPathogen] = useState<string>('Fungal')
  const [diceCrops] = useState<string[]>(['Rice'])
  const [dicePathogens] = useState<string[]>(['Fungal', 'Bacterial'])
  const [diceMinContrast, setDiceMinContrast] = useState<number>(0.0)
  const [pivotMeasure, setPivotMeasure] = useState<string>('observation_count')

  useEffect(() => {
    runQuery('rollup')
  }, [])

  const runQuery = (op: string) => {
    setLoading(true)
    let body: any = { operation: op }

    if (op === 'rollup') {
      body.operation = 'rollup'
    } else if (op === 'true_drilldown') {
      body.operation = 'true_drilldown'
      body.pathogen_type = trueDrilldownPathogen
    } else if (op === 'diagnostic_drilldown') {
      body.operation = 'diagnostic_drilldown'
      body.crop_category = drilldownCategory !== 'All' ? drilldownCategory : undefined
    } else if (op === 'slice_crop') {
      body.operation = 'slice_crop'
      body.crop_name = sliceCrop
    } else if (op === 'slice_pathogen') {
      body.operation = 'slice_pathogen'
      body.pathogen_type = slicePathogen
    } else if (op === 'dice') {
      body.operation = 'dice'
      body.selected_crops = diceCrops
      body.selected_pathogens = dicePathogens
      body.min_contrast = diceMinContrast
    } else if (op === 'pivot') {
      body.operation = 'pivot'
      body.pivot_measure = pivotMeasure
    }

    api
      .executeOLAPQuery(body)
      .then((res) => {
        setQueryResult(res)
        setLoading(false)
      })
      .catch((err) => {
        console.error('OLAP query error:', err)
        setLoading(false)
      })
  }

  const handleOpChange = (op: string) => {
    setActiveOp(op)
    runQuery(op)
  }

  return (
    <div className="flex flex-col gap-6 max-w-[1720px] mx-auto w-full pb-12">
      {/* Top Banner */}
      <section className="bg-white rounded-2xl p-6 border border-[#E2E7DF] shadow-xs flex flex-col gap-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#E0F2E8] text-[#175D44] flex items-center justify-center">
              <span className="material-symbols-outlined text-[24px]">view_in_ar</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-headline text-xl font-bold text-[#0F1F18]">
                  Multimodal OLAP Analytics Workbench
                </h1>
                <span className="px-2 py-0.5 rounded-full font-mono text-[10px] bg-[#E0F2E8] text-[#175D44] font-bold">
                  ANSI SQL Engine
                </span>
              </div>
              <p className="text-xs text-[#404943]">
                Direct dimensional hypercube operations: Roll-up, Drill-down, Slice, Dice, and Pivot over SQLite
              </p>
            </div>
          </div>
        </div>

        {/* OLAP Operation Switcher Pills */}
        <div className="flex flex-wrap items-center gap-2 pt-3 border-t border-[#E2E7DF]">
          {[
            { id: 'rollup', label: '1. Roll-Up', desc: 'Observation -> Crop Category' },
            { id: 'true_drilldown', label: '2A. True Drill-Down', desc: 'Pathogen -> Disease' },
            { id: 'diagnostic_drilldown', label: '2B. Diagnostic Drill-Across', desc: 'Multi-attribute' },
            { id: 'slice_crop', label: '3A. Slice (Crop)', desc: 'Crop Dimension Plane' },
            { id: 'slice_pathogen', label: '3B. Slice (Pathogen)', desc: 'Pathogen Plane' },
            { id: 'dice', label: '4. Dice Sub-Cube', desc: 'Crop × Pathogen × Contrast' },
            { id: 'pivot', label: '5. Pivot Matrix', desc: 'Crops × Pathogen Types' },
          ].map((op) => (
            <button
              key={op.id}
              onClick={() => handleOpChange(op.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                activeOp === op.id
                  ? 'bg-[#175D44] text-white shadow-sm'
                  : 'bg-[#F7F6EF] text-[#404943] hover:text-[#0F1F18] border border-[#E2E7DF]'
              }`}
            >
              <span>{op.label}</span>
            </button>
          ))}
        </div>
      </section>

      {/* Dynamic Slicer Parameters for Selected Operation */}
      <div className="bg-white rounded-xl p-4 border border-[#E2E7DF] flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-4 text-xs">
          {activeOp === 'slice_crop' && (
            <div className="flex items-center gap-2">
              <span className="font-mono text-[#404943]">Slice Crop:</span>
              <select
                value={sliceCrop}
                onChange={(e) => setSliceCrop(e.target.value)}
                className="px-2.5 py-1 rounded bg-[#F7F6EF] border border-[#E2E7DF] font-semibold text-[#0F1F18]"
              >
                <option value="Rice">Rice (Oryza sativa)</option>
              </select>
            </div>
          )}

          {activeOp === 'slice_pathogen' && (
            <div className="flex items-center gap-2">
              <span className="font-mono text-[#404943]">Pathogen Dimension:</span>
              <select
                value={slicePathogen}
                onChange={(e) => setSlicePathogen(e.target.value)}
                className="px-2.5 py-1 rounded bg-[#F7F6EF] border border-[#E2E7DF] font-semibold text-[#0F1F18]"
              >
                <option value="Fungal">Fungal (Brown Spot, Leaf Smut)</option>
                <option value="Bacterial">Bacterial (Bacterial Leaf Blight)</option>
              </select>
            </div>
          )}

          {activeOp === 'true_drilldown' && (
            <div className="flex items-center gap-2">
              <span className="font-mono text-[#404943]">Filter Pathogen Level:</span>
              <select
                value={trueDrilldownPathogen}
                onChange={(e) => setTrueDrilldownPathogen(e.target.value)}
                className="px-2.5 py-1 rounded bg-[#F7F6EF] border border-[#E2E7DF] font-semibold text-[#0F1F18]"
              >
                <option value="All">All Pathogen Types</option>
                <option value="Fungal">Fungal</option>
                <option value="Bacterial">Bacterial</option>
              </select>
            </div>
          )}

          {activeOp === 'diagnostic_drilldown' && (
            <div className="flex items-center gap-2">
              <span className="font-mono text-[#404943]">Crop Category Level:</span>
              <select
                value={drilldownCategory}
                onChange={(e) => setDrilldownCategory(e.target.value)}
                className="px-2.5 py-1 rounded bg-[#F7F6EF] border border-[#E2E7DF] font-semibold text-[#0F1F18]"
              >
                <option value="All">All Categories</option>
                <option value="Cereal">Cereal</option>
              </select>
            </div>
          )}

          {activeOp === 'dice' && (
            <>
              <div className="flex items-center gap-2">
                <span className="font-mono text-[#404943]">Min Texture Contrast:</span>
                <input
                  type="range"
                  min="0.0"
                  max="50.0"
                  step="5.0"
                  value={diceMinContrast}
                  onChange={(e) => setDiceMinContrast(parseFloat(e.target.value))}
                  className="w-24 accent-[#175D44]"
                />
                <span className="font-mono font-bold text-[#175D44]">{diceMinContrast}</span>
              </div>
            </>
          )}

          {activeOp === 'pivot' && (
            <div className="flex items-center gap-2">
              <span className="font-mono text-[#404943]">Pivot Measure:</span>
              <select
                value={pivotMeasure}
                onChange={(e) => setPivotMeasure(e.target.value)}
                className="px-2.5 py-1 rounded bg-[#F7F6EF] border border-[#E2E7DF] font-semibold text-[#0F1F18]"
              >
                <option value="observation_count">Observation Count</option>
                <option value="avg_severity">Average Lesion Severity</option>
                <option value="avg_contrast">Mean GLCM Texture Contrast</option>
              </select>
            </div>
          )}
        </div>

        <button
          onClick={() => runQuery(activeOp)}
          className="px-3.5 py-1.5 rounded-lg bg-[#175D44] text-white hover:bg-[#34765B] font-semibold text-xs flex items-center gap-1.5 transition-colors shadow-xs"
        >
          <span className="material-symbols-outlined text-[15px]">play_arrow</span>
          <span>Execute OLAP Query</span>
        </button>
      </div>

      {/* SQL Execution Output Box */}
      {queryResult && (
        <div className="bg-[#1E1E1E] rounded-xl p-4 text-[#D4D4D4] font-mono text-xs shadow-md border border-[#333333]">
          <div className="flex items-center justify-between pb-2 mb-2 border-b border-[#333333] text-[11px]">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#C3EFAA]"></span>
              <span className="text-[#C3EFAA] font-bold">{queryResult.operation}</span>
              <span className="text-[#888888]">| {queryResult.hierarchy || 'Hypercube Operation'}</span>
            </div>
            <div className="flex items-center gap-3">
              <span>
                Latency:{' '}
                <strong className="text-[#ADF1D0]">{queryResult.latency_ms} ms</strong>
              </span>
              <span>
                Row count:{' '}
                <strong className="text-white">{queryResult.row_count}</strong>
              </span>
            </div>
          </div>
          <pre className="overflow-x-auto whitespace-pre-wrap text-[#9CDCFE] leading-relaxed">
            {queryResult.sql}
          </pre>
        </div>
      )}

      {/* Tabular Result Set */}
      <SectionCard
        moduleNumber="Hypercube Result Matrix"
        title={`${queryResult?.operation ?? 'OLAP'} Result Set`}
        subtitle={`Computed against relational star schema (${queryResult?.row_count ?? 0} rows)`}
        badge={queryResult ? `${queryResult.latency_ms} ms` : undefined}
      >
        {loading ? (
          <div className="flex items-center justify-center py-12 gap-2 text-xs text-[#404943]">
            <span className="material-symbols-outlined animate-spin text-[18px]">progress_activity</span>
            <span>Executing dimensional SQL query...</span>
          </div>
        ) : queryResult && queryResult.data.length > 0 ? (
          <div className="border border-[#E2E7DF] rounded-xl overflow-hidden bg-white">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-[#E5F8ED] text-[#175D44] font-mono text-[11px] border-b border-[#E2E7DF]">
                  <tr>
                    {queryResult.columns.map((col) => (
                      <th key={col} className="py-2.5 px-3.5 font-semibold capitalize">
                        {col.replace(/_/g, ' ')}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E2E7DF]">
                  {queryResult.data.map((row, idx) => (
                    <tr key={idx} className="hover:bg-[#F7F6EF] transition-colors">
                      {queryResult.columns.map((col) => {
                        const val = row[col]
                        const isNum = typeof val === 'number'
                        return (
                          <td
                            key={col}
                            className={`py-2 px-3.5 ${
                              isNum ? 'font-mono text-[#175D44] font-medium' : 'text-[#0F1F18]'
                            }`}
                          >
                            {isNum ? (Number.isInteger(val) ? val : val.toFixed(4)) : val ?? '—'}
                          </td>
                        )
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ) : (
          <div className="text-center py-8 text-xs text-[#404943]">
            No records returned for the current slice parameters.
          </div>
        )}
      </SectionCard>
    </div>
  )
}
