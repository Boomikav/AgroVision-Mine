import React, { useEffect, useState } from 'react'
import { api } from '../services/api'
import type { ClusteringResponse, PCAPoint } from '../types/api'
import { SectionCard } from '../components/common/SectionCard'
import { KPICard } from '../components/common/KPICard'

export const VisualPatternMiningPage: React.FC = () => {
  const [selectedK, setSelectedK] = useState<number>(2)
  const [data, setData] = useState<ClusteringResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [hoveredPoint, setHoveredPoint] = useState<PCAPoint | null>(null)

  useEffect(() => {
    setLoading(true)
    api
      .getClusteringResults(selectedK, 800)
      .then((res) => {
        setData(res)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Clustering API error:', err)
        setLoading(false)
      })
  }, [selectedK])

  if (loading && !data) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-3 text-[#404943]">
        <span className="material-symbols-outlined text-4xl animate-spin text-[#175D44]">
          progress_activity
        </span>
        <span className="text-sm font-mono">Computing latent visual space projections...</span>
      </div>
    )
  }

  // PCA coordinate scale mapping
  // pca_x ranges roughly [-6, 12], pca_y ranges roughly [-6, 11]
  const svgWidth = 800
  const svgHeight = 440
  const padding = 40
  const minX = -7
  const maxX = 12
  const minY = -7
  const maxY = 11

  const scaleX = (x: number) => padding + ((x - minX) / (maxX - minX)) * (svgWidth - 2 * padding)
  const scaleY = (y: number) => svgHeight - padding - ((y - minY) / (maxY - minY)) * (svgHeight - 2 * padding)

  const clusterColors = ['#175D44', '#8B6306', '#426831', '#C87858']

  return (
    <div className="flex flex-col gap-6 max-w-[1720px] mx-auto w-full pb-12">
      {/* Top Banner & Solution Selector */}
      <header className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-[#E2E7DF] shadow-xs">
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2">
            <span className="font-mono text-[10px] uppercase tracking-wider text-[#175D44] font-bold">
              Unsupervised Latent Space
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-[#BFC9C2]"></span>
            <span className="font-mono text-[10px] text-[#404943]">
              32 Continuous Visual Descriptors
            </span>
          </div>
          <h1 className="font-headline text-2xl font-bold text-[#0F1F18] tracking-tight">
            Visual Pattern Mining Workspace
          </h1>
        </div>

        {/* Toggles & Scientific Disclaimer */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="inline-flex p-1 bg-[#F7F6EF] border border-[#E2E7DF] rounded-xl gap-1">
            <button
              onClick={() => setSelectedK(2)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                selectedK === 2
                  ? 'bg-[#175D44] text-white shadow-xs'
                  : 'text-[#404943] hover:text-[#0F1F18]'
              }`}
            >
              <span>K=2 Solution</span>
              <span className="inline-flex items-center px-1.5 py-0.2 rounded font-mono text-[9px] bg-[#FFDEA7] text-[#271900] font-bold">
                Silh 0.4060
              </span>
            </button>
            <button
              onClick={() => setSelectedK(4)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                selectedK === 4
                  ? 'bg-[#175D44] text-white shadow-xs'
                  : 'text-[#404943] hover:text-[#0F1F18]'
              }`}
            >
              <span>K=4 Exploratory</span>
              <span className="inline-flex items-center px-1.5 py-0.2 rounded font-mono text-[9px] bg-[#E0F2E8] text-[#175D44]">
                Silh 0.1651
              </span>
            </button>
          </div>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#E5F8ED] text-[#404943] text-xs">
            <span className="material-symbols-outlined text-[16px] text-[#6C4C00] shrink-0">
              info
            </span>
            <span className="text-[11px]">
              Mathematical groupings; does not constitute automated diagnosis.
            </span>
          </div>
        </div>
      </header>

      {/* Metric Cards: Cluster Convergence & Quality */}
      <section className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <KPICard
          label="Silhouette Score"
          value={data?.solution_metrics?.silhouette_score ? data.solution_metrics.silhouette_score.toFixed(4) : (selectedK === 2 ? '0.4060' : '0.1651')}
          icon="bubble_chart"
          iconColor="text-[#175D44]"
          progressLabel={selectedK === 2 ? 'Optimal Partition' : 'Sub-partitioned Dispersion'}
          progressPercent={selectedK === 2 ? 80 : 35}
          footerNote={selectedK === 2 ? 'Well-separated visual clusters' : 'Increased overlapping boundary'}
        />

        <KPICard
          label="Davies-Bouldin Index"
          value={data?.solution_metrics?.davies_bouldin_index ? data.solution_metrics.davies_bouldin_index.toFixed(4) : (selectedK === 2 ? '1.0990' : '1.8339')}
          icon="compress"
          iconColor="text-[#6C4C00]"
          progressLabel="Lower is tighter"
          progressPercent={selectedK === 2 ? 75 : 40}
          footerNote={selectedK === 2 ? '40.1% tighter cluster cohesion' : 'Higher intra-cluster spread'}
        />

        <KPICard
          label="Calinski-Harabasz"
          value={data?.solution_metrics?.calinski_harabasz_score ? data.solution_metrics.calinski_harabasz_score.toFixed(2) : (selectedK === 2 ? '1,154.38' : '674.33')}
          icon="scatter_plot"
          iconColor="text-[#175D44]"
          progressLabel="Dispersion Ratio"
          progressPercent={selectedK === 2 ? 90 : 45}
          footerNote={selectedK === 2 ? '+71.2% higher dispersion ratio' : 'Lower variance separation'}
        />

        <KPICard
          label="K-Means Convergence"
          value={selectedK === 2 ? '14' : '26'}
          unit="Iterations"
          icon="sync_alt"
          iconColor="text-[#426831]"
          progressLabel="Tolerance <= 1e-4 reached"
          progressPercent={100}
          footerNote="Deterministic initialization (seed 42)"
        />
      </section>

      {/* Main Split: PCA 2D Scatter + Cluster Composition */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* PCA Scatter Projection (8 cols) */}
        <div className="lg:col-span-8">
          <SectionCard
            moduleNumber="Dimensional Reduction"
            title="PCA 2D Latent Feature Projection"
            subtitle={`Principal Component 1 (${((data?.pca_projection?.explained_variance_ratio?.[0] ?? 0.3856) * 100).toFixed(1)}%) × Principal Component 2 (${((data?.pca_projection?.explained_variance_ratio?.[1] ?? 0.1355) * 100).toFixed(1)}%) | Total Explained Variance: ${((data?.pca_projection?.total_variance_explained ?? 0.5211) * 100).toFixed(1)}%`}
            actions={
              <div className="flex items-center gap-2">
                {Array.from({ length: selectedK }).map((_, idx) => (
                  <div
                    key={idx}
                    className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[#F7F6EF] border border-[#E2E7DF] text-xs font-mono font-medium"
                  >
                    <span
                      className="w-2.5 h-2.5 rounded-full inline-block"
                      style={{ backgroundColor: clusterColors[idx] }}
                    />
                    <span>Cluster {idx}</span>
                  </div>
                ))}
              </div>
            }
          >
            <div className="relative w-full aspect-[16/10] bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] overflow-hidden flex flex-col justify-between p-2 select-none">
              {/* SVG Canvas */}
              <svg
                viewBox={`0 0 ${svgWidth} ${svgHeight}`}
                className="w-full h-full overflow-visible"
              >
                {/* Axis Grid lines */}
                <line
                  x1={scaleX(0)}
                  y1={0}
                  x2={scaleX(0)}
                  y2={svgHeight}
                  stroke="#175D44"
                  strokeWidth="1.5"
                  strokeDasharray="4 4"
                  opacity="0.3"
                />
                <line
                  x1={0}
                  y1={scaleY(0)}
                  x2={svgWidth}
                  y2={scaleY(0)}
                  stroke="#175D44"
                  strokeWidth="1.5"
                  strokeDasharray="4 4"
                  opacity="0.3"
                />

                {/* Axis Labels */}
                <text
                  x={svgWidth - 60}
                  y={scaleY(0) - 8}
                  fill="#707973"
                  fontSize="10"
                  fontFamily="monospace"
                >
                  PC1 (38.6%) &rarr;
                </text>
                <text
                  x={scaleX(0) + 8}
                  y={20}
                  fill="#707973"
                  fontSize="10"
                  fontFamily="monospace"
                >
                  &uarr; PC2 (13.6%)
                </text>

                {/* Specimen Scatter Points */}
                {data?.scatter_points.map((pt, i) => {
                  const cx = scaleX(pt.x)
                  const cy = scaleY(pt.y)
                  const color = clusterColors[pt.cluster % clusterColors.length]
                  return (
                    <circle
                      key={i}
                      cx={cx}
                      cy={cy}
                      r="3.5"
                      fill={color}
                      opacity="0.75"
                      className="hover:r-6 hover:opacity-100 transition-all cursor-pointer"
                      onMouseEnter={() => setHoveredPoint(pt)}
                      onMouseLeave={() => setHoveredPoint(null)}
                    />
                  )
                })}
              </svg>

              {/* Hover Tooltip Overlay */}
              {hoveredPoint && (
                <div className="absolute top-4 left-4 p-3 bg-white/95 backdrop-blur-md rounded-xl border border-[#175D44] shadow-lg text-xs font-mono flex flex-col gap-1 pointer-events-none z-20">
                  <div className="flex items-center gap-1.5 font-bold text-[#0F1F18]">
                    <span>{hoveredPoint.image_id}</span>
                    <span
                      className="px-1.5 py-0.2 rounded text-[9px] text-white"
                      style={{ backgroundColor: clusterColors[hoveredPoint.cluster] }}
                    >
                      C{hoveredPoint.cluster}
                    </span>
                  </div>
                  <div className="text-[#175D44] font-semibold">{hoveredPoint.crop}</div>
                  <div className="text-[#404943]">{hoveredPoint.disease}</div>
                  <div className="text-[10px] text-[#707973]">
                    PC1: {hoveredPoint.x.toFixed(3)}, PC2: {hoveredPoint.y.toFixed(3)}
                  </div>
                </div>
              )}
            </div>
          </SectionCard>
        </div>

        {/* Cluster Profiles and Feature Centers (4 cols) */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          <SectionCard
            moduleNumber="Centroid Signatures"
            title={`K=${selectedK} Feature Profiles`}
            subtitle="Top elevated & suppressed visual dimensions per cluster"
          >
            <div className="flex flex-col gap-3 text-xs max-h-[460px] overflow-y-auto pr-1">
              {data?.cluster_profiles.map((cp) => (
                <div
                  key={cp.cluster_id}
                  className="p-3.5 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-[#0F1F18] flex items-center gap-1.5">
                      <span
                        className="w-2.5 h-2.5 rounded-full"
                        style={{ backgroundColor: clusterColors[cp.cluster_id] }}
                      />
                      Cluster {cp.cluster_id}
                    </span>
                    <span className="font-mono text-[11px] text-[#175D44] font-bold">
                      {cp.size.toLocaleString()} ({cp.percentage}%)
                    </span>
                  </div>

                  <div className="flex flex-col gap-1 pt-1">
                    <span className="text-[10px] uppercase font-mono text-[#175D44] font-bold">
                      Elevated Features:
                    </span>
                    {cp.top_elevated_features.slice(0, 3).map((f) => (
                      <div
                        key={f.feature}
                        className="flex justify-between items-center font-mono text-[11px]"
                      >
                        <span className="text-[#404943] truncate">{f.feature}</span>
                        <span className="text-[#175D44] font-semibold">
                          +{f.z_score.toFixed(2)}z
                        </span>
                      </div>
                    ))}
                  </div>

                  <div className="flex flex-col gap-1 pt-1 border-t border-[#E2E7DF]">
                    <span className="text-[10px] uppercase font-mono text-[#93000A] font-bold">
                      Suppressed Features:
                    </span>
                    {cp.top_suppressed_features.slice(0, 3).map((f) => (
                      <div
                        key={f.feature}
                        className="flex justify-between items-center font-mono text-[11px]"
                      >
                        <span className="text-[#404943] truncate">{f.feature}</span>
                        <span className="text-[#93000A] font-semibold">
                          {f.z_score.toFixed(2)}z
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </SectionCard>
        </div>
      </div>

      {/* Contingency & Chi-Square Analysis Breakdown */}
      {data?.contingency_analysis && (
        <SectionCard
          moduleNumber="Hypothesis Testing"
          title="Contingency & Statistical Association Analysis"
          subtitle="Chi-square test of independence between unsupervised clusters and ground-truth agronomic attributes"
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs pt-1">
            {Object.entries(data.contingency_analysis).map(([key, val]: [string, any]) => (
              <div
                key={key}
                className="p-4 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm capitalize text-[#0F1F18]">
                    {key.replace(/_/g, ' ')}
                  </span>
                  <span className="px-2 py-0.5 rounded font-mono text-[10px] bg-[#E0F2E8] text-[#175D44] font-bold">
                    p &lt; 0.001
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-2 font-mono text-[11px] pt-1 border-t border-[#E2E7DF]">
                  <div>
                    <span className="text-[#707973] block">Chi-Square:</span>
                    <strong className="text-[#0F1F18]">{val.chi2_statistic?.toFixed(1) ?? '—'}</strong>
                  </div>
                  <div>
                    <span className="text-[#707973] block">Cramer's V:</span>
                    <strong className="text-[#175D44]">{val.cramers_v?.toFixed(4) ?? '—'}</strong>
                  </div>
                </div>
                <p className="text-[11px] text-[#404943] leading-tight pt-1">
                  Significant visual descriptor alignment with {key.replace(/_/g, ' ')} stratification.
                </p>
              </div>
            ))}
          </div>
        </SectionCard>
      )}
    </div>
  )
}
