import React, { useEffect, useState } from 'react'
import { api } from '../services/api'
import type { OverviewResponse } from '../types/api'
import { KPICard } from '../components/common/KPICard'
import { SectionCard } from '../components/common/SectionCard'
import type { PageId } from '../components/layout/Sidebar'

interface OverviewPageProps {
  onNavigate: (page: PageId) => void
}

export const OverviewPage: React.FC<OverviewPageProps> = ({ onNavigate }) => {
  const [data, setData] = useState<OverviewResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api
      .getOverview()
      .then((res) => {
        setData(res)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load overview:', err)
        setLoading(false)
      })
  }, [])

  if (loading || !data) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-3 text-[#404943]">
        <span className="material-symbols-outlined text-4xl animate-spin text-[#175D44]">
          progress_activity
        </span>
        <span className="text-sm font-mono">Loading AgroVision-Mine Overview telemetry...</span>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6 max-w-[1720px] mx-auto w-full pb-12">
      {/* Section 1: Editorial Welcome Banner */}
      <section className="relative bg-[#E5F8ED]/60 rounded-2xl p-6 sm:p-8 border border-[#BFC9C2]/40 overflow-hidden shadow-xs">
        <div className="absolute -right-16 -top-24 w-96 h-96 rounded-full bg-[#C3EFAA]/30 pointer-events-none blur-3xl" />
        <div className="absolute right-48 -bottom-20 w-80 h-80 rounded-full bg-[#ADF1D0]/30 pointer-events-none blur-2xl" />

        <div className="relative z-10 flex flex-col xl:flex-row xl:items-end justify-between gap-6">
          <div className="max-w-3xl flex flex-col gap-2">
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-[#D4E7DC] text-[#6C4C00] font-mono text-[10px] uppercase tracking-wider font-semibold">
                <span className="w-1.5 h-1.5 rounded-full bg-[#6C4C00]"></span>
                Academic Research Artifact • Frozen Dataset v2
              </span>
              <span className="font-mono text-[10px] text-[#404943]">
                SHA-256 Checksum Verified Invariant
              </span>
            </div>
            <h1 className="font-headline text-3xl sm:text-4xl text-[#0F1F18] font-bold tracking-tight">
              From crop imagery to actionable insight
            </h1>
            <p className="text-sm text-[#404943] leading-relaxed max-w-2xl">
              Multimodal Data Warehouse and Visual Pattern Mining framework for crop pathology and pest intelligence. Integrates dimensional OLAP cubes with explainable 32-dimensional computer vision features across 2,596 verified leaf specimens.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            <button
              onClick={() => onNavigate('olap-analytics')}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-[#175D44] text-white font-semibold text-xs hover:bg-[#34765B] transition-all shadow-sm"
            >
              <span className="material-symbols-outlined text-[18px]">view_in_ar</span>
              <span>Launch OLAP Workbench</span>
            </button>
            <button
              onClick={() => onNavigate('dataset-explorer')}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-white text-[#0F1F18] border border-[#BFC9C2]/60 font-semibold text-xs hover:bg-[#F7F6EF] transition-all shadow-sm"
            >
              <span className="material-symbols-outlined text-[18px]">travel_explore</span>
              <span>Explore 2,596 Records</span>
            </button>
          </div>
        </div>
      </section>

      {/* Section 2: Prominent KPI Metric Cards */}
      <section className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {/* KPI 1: Corpus Size */}
        <KPICard
          label="Corpus Size"
          value={data.corpus_size}
          icon="photo_library"
          iconColor="text-[#175D44]"
          progressLabel={`PlantDoc: ${data.sources.plantdoc.toLocaleString()} (98.6%)`}
          secondaryLabel={`ICAR: ${data.sources.icar_ogd}`}
          progressPercent={data.sources.plantdoc_percentage}
          footerNote="100% SHA-256 authentic rasters"
        />

        {/* KPI 2: Botanical Taxa */}
        <KPICard
          label="Botanical Taxa"
          value={data.taxa_count}
          unit="Crops"
          icon="potted_plant"
          iconColor="text-[#426831]"
          progressLabel="Solanum • Zea • Malus • Vitis"
          secondaryLabel="14 Genera"
          progressPercent={100}
          footerNote="Monocots & Eudicots Stratified"
        />

        {/* KPI 3: Pathological Status */}
        <KPICard
          label="Pathological Status"
          value={data.pathological_status.diseased}
          unit={`Diseased (${data.pathological_status.diseased_percentage}%)`}
          icon="coronavirus"
          iconColor="text-[#BA1A1A]"
          progressLabel={`${data.pathological_status.healthy} Healthy (32.6%)`}
          secondaryLabel="1,750 Lesion"
          progressPercent={data.pathological_status.diseased_percentage}
          footerNote="Annotated symptomatic leaves"
        />

        {/* KPI 4: Feature Dimensions */}
        <KPICard
          label="Feature Dimensions"
          value={data.feature_dimensions.continuous_count}
          unit="Vector Dims"
          icon="hub"
          iconColor="text-[#6C4C00]"
          progressLabel="Color (9) • GLCM (16) • Hu (7)"
          secondaryLabel="Standardized"
          progressPercent={100}
          footerNote="Zero mean, unit variance z-score"
        />
      </section>

      {/* Section 3: Analytical Breakdown Modules */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Module 1: Dataset Composition (7 cols) */}
        <div className="lg:col-span-7">
          <SectionCard
            moduleNumber="Analytical Module 01"
            title="Dataset Composition & Health Breakdown"
            subtitle="Distribution of symptomatic pathological specimens versus healthy asymptomatic baselines"
            badge={`N = ${data.corpus_size.toLocaleString()}`}
          >
            <div className="grid grid-cols-1 sm:grid-cols-12 gap-6 items-center pt-2">
              {/* Donut Graphic */}
              <div className="sm:col-span-5 flex flex-col items-center justify-center p-4 bg-[#F7F6EF] rounded-xl border border-[#E2E7DF]">
                <div className="relative w-36 h-36 flex items-center justify-center">
                  <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
                    <circle
                      className="text-[#E0F2E8]"
                      cx="50"
                      cy="50"
                      fill="none"
                      r="38"
                      stroke="currentColor"
                      strokeWidth="12"
                    />
                    {/* Diseased arc 67.4% */}
                    <circle
                      className="text-[#BA1A1A]"
                      cx="50"
                      cy="50"
                      fill="none"
                      r="38"
                      stroke="currentColor"
                      strokeDasharray="160.9 238.8"
                      strokeLinecap="round"
                      strokeWidth="12"
                    />
                    {/* Healthy arc 32.6% */}
                    <circle
                      className="text-[#426831]"
                      cx="50"
                      cy="50"
                      fill="none"
                      r="38"
                      stroke="currentColor"
                      strokeDasharray="77.8 238.8"
                      strokeDashoffset="-160.9"
                      strokeLinecap="round"
                      strokeWidth="12"
                    />
                  </svg>
                  <div className="absolute flex flex-col items-center text-center">
                    <span className="font-headline text-xl font-bold text-[#0F1F18] leading-none">
                      {data.pathological_status.diseased_percentage}%
                    </span>
                    <span className="font-mono text-[9px] text-[#404943] uppercase mt-0.5">
                      Pathology
                    </span>
                  </div>
                </div>

                <div className="mt-3 w-full flex flex-col gap-1.5 px-1 text-xs">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5">
                      <span className="w-2.5 h-2.5 rounded-full bg-[#BA1A1A]" />
                      <span className="text-[#0F1F18]">Diseased Specimen</span>
                    </div>
                    <span className="font-mono font-medium text-[#0F1F18]">
                      {data.pathological_status.diseased.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5">
                      <span className="w-2.5 h-2.5 rounded-full bg-[#426831]" />
                      <span className="text-[#0F1F18]">Healthy Baseline</span>
                    </div>
                    <span className="font-mono font-medium text-[#0F1F18]">
                      {data.pathological_status.healthy.toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>

              {/* Horizontal Bar Chart of Top Crops */}
              <div className="sm:col-span-7 flex flex-col gap-3">
                <div className="flex items-center justify-between text-xs text-[#404943] font-mono">
                  <span className="uppercase font-semibold">Top Represented Crop Genomes</span>
                  <span>Count</span>
                </div>

                {data.top_crops.map((crop) => (
                  <div key={crop.crop} className="flex flex-col gap-1">
                    <div className="flex justify-between text-xs">
                      <span className="font-medium text-[#0F1F18]">{crop.crop}</span>
                      <span className="font-mono text-[#404943]">
                        {crop.count} ({crop.percentage}%)
                      </span>
                    </div>
                    <div className="w-full h-2 rounded bg-[#E0F2E8] overflow-hidden">
                      <div
                        className="bg-[#175D44] h-full rounded transition-all duration-500"
                        style={{ width: `${(crop.count / data.top_crops[0].count) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </SectionCard>
        </div>

        {/* Module 2: Provenance Audit & Imbalance (5 cols) */}
        <div className="lg:col-span-5">
          <SectionCard
            moduleNumber="Provenance Audit"
            title="Cross-Source Distribution & Caveats"
            subtitle="Verified provenance across two heterogenous agricultural data archives"
            badge="Verified Integrity"
          >
            <div className="flex flex-col gap-4 text-xs">
              <div className="p-3.5 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-[#0F1F18] flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-[#175D44]"></span>
                    PlantDoc Benchmark
                  </span>
                  <span className="font-mono font-bold text-[#175D44]">2,560 images (98.6%)</span>
                </div>
                <p className="text-[#404943] leading-relaxed text-[11px]">
                  Unconstrained in-the-field photographic capture across diverse agricultural conditions, natural backgrounds, varying lighting, and multi-crop foliage.
                </p>
              </div>

              <div className="p-3.5 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-[#0F1F18] flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-[#6C4C00]"></span>
                    ICAR / Open Government Data India
                  </span>
                  <span className="font-mono font-bold text-[#6C4C00]">36 images (1.4%)</span>
                </div>
                <p className="text-[#404943] leading-relaxed text-[11px]">
                  High-resolution macro laboratory captures focusing on cereal pathology (Rice Brown Spot, Leaf Smut, Bacterial Blight).
                </p>
              </div>

              {/* Scientific Caveats Alert */}
              <div className="p-3 rounded-lg bg-[#FFDEA7]/30 border border-[#FFDEA7] text-[11px] text-[#6C4C00] flex items-start gap-2">
                <span className="material-symbols-outlined text-[16px] shrink-0 mt-0.5">
                  info
                </span>
                <p className="leading-relaxed">
                  <strong>Scientific Disclosure:</strong> Dataset dominance belongs to PlantDoc. Rice is exclusively represented via ICAR. Pest symptoms represent an underrepresented minority class (2 specimens).
                </p>
              </div>
            </div>
          </SectionCard>
        </div>
      </div>

      {/* Section 4: Mining & Unsupervised Latent Space Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SectionCard
          moduleNumber="Pattern Mining"
          title="K-Means Visual Clustering Benchmark"
          subtitle="Unsupervised mathematical feature clustering over 32 continuous descriptors"
          actions={
            <button
              onClick={() => onNavigate('visual-pattern-mining')}
              className="text-xs text-[#175D44] hover:underline font-semibold flex items-center gap-1"
            >
              <span>Explore Workspace</span>
              <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
            </button>
          }
        >
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="p-3 rounded-lg bg-[#E0F2E8]/60 border border-[#BFC9C2]/30 flex flex-col gap-1">
              <span className="font-mono text-[10px] text-[#404943] uppercase">Primary Solution</span>
              <span className="font-headline font-bold text-lg text-[#175D44]">K = 2 (Optimal)</span>
              <span className="text-[11px] text-[#404943]">
                Silhouette: <strong className="font-mono text-[#0F1F18]">0.4060</strong>
              </span>
              <span className="text-[10px] text-[#426831] font-medium">Davies-Bouldin: 1.0990</span>
            </div>

            <div className="p-3 rounded-lg bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-1">
              <span className="font-mono text-[10px] text-[#404943] uppercase">Exploratory Partition</span>
              <span className="font-headline font-bold text-lg text-[#404943]">K = 4 (Sub-partition)</span>
              <span className="text-[11px] text-[#404943]">
                Silhouette: <strong className="font-mono text-[#0F1F18]">0.1651</strong>
              </span>
              <span className="text-[10px] text-[#404943]">Davies-Bouldin: 1.8339</span>
            </div>
          </div>
          <p className="text-[11px] text-[#404943] mt-3 leading-relaxed">
            2D PCA projection captures <strong>52.1%</strong> total visual variance (PC1: 38.6%, PC2: 13.6%). Clusters represent mathematical density groups, not automated biological diagnoses.
          </p>
        </SectionCard>

        <SectionCard
          moduleNumber="Association Mining"
          title="Apriori & FP-Growth Rule Mining"
          subtitle="Discovery of frequent co-occurrence itemsets across discretized visual features"
          actions={
            <button
              onClick={() => onNavigate('association-rules')}
              className="text-xs text-[#175D44] hover:underline font-semibold flex items-center gap-1"
            >
              <span>Explore Rules</span>
              <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
            </button>
          }
        >
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="p-3 rounded-lg bg-[#E0F2E8]/60 border border-[#BFC9C2]/30 flex flex-col gap-1">
              <span className="font-mono text-[10px] text-[#404943] uppercase">Mode A: Visual-Only</span>
              <span className="font-headline font-bold text-lg text-[#175D44]">880 Rules</span>
              <span className="text-[11px] text-[#404943]">Strictly unsupervised</span>
              <span className="text-[10px] text-[#426831] font-medium">100% Rule Parity Verified</span>
            </div>

            <div className="p-3 rounded-lg bg-[#FFDEA7]/30 border border-[#FFDEA7] flex flex-col gap-1">
              <span className="font-mono text-[10px] text-[#6C4C00] uppercase">Mode B: Labeled</span>
              <span className="font-headline font-bold text-lg text-[#6C4C00]">285 Rules</span>
              <span className="text-[11px] text-[#404943]">Exploratory with labels</span>
              <span className="text-[10px] text-[#6C4C00] font-medium">Terracotta Disclosure Flag</span>
            </div>
          </div>
          <p className="text-[11px] text-[#404943] mt-3 leading-relaxed">
            FP-Growth and Apriori achieve 100% mathematical output equivalence (880 visual rules, max diff = 0.0) with execution under 0.35s on 2,596 transactions.
          </p>
        </SectionCard>
      </div>

      {/* Section 5: End-to-End Pipeline Architecture */}
      <SectionCard
        moduleNumber="System Architecture"
        title="AgroVision-Mine End-to-End Pipeline Architecture"
        subtitle="Reproducible data flow from heterogeneous raw rasters to OLAP hypercube and visual pattern mining"
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 pt-2">
          {[
            {
              step: '01',
              title: 'Acquisition & Validation',
              detail: '2,596 Authentic Images from PlantDoc & ICAR/OGD. Corruptions: 0.',
              icon: 'dataset',
            },
            {
              step: '02',
              title: 'Quality Gates & Cleaning',
              detail: 'Laplacian variance blur audit, uniform 256x256 resizing, metadata normalization.',
              icon: 'rule',
            },
            {
              step: '03',
              title: 'Visual Feature Store',
              detail: '32 continuous features (Color Moments, GLCM Haralick, Hu Contours). Standardized z-score.',
              icon: 'auto_awesome_motion',
            },
            {
              step: '04',
              title: 'Star Schema Warehouse',
              detail: 'SQLite 3 dimensional model (4 dimension tables + 1 fact table). Foreign keys enforced.',
              icon: 'database',
            },
            {
              step: '05',
              title: 'OLAP & Mining Engine',
              detail: 'Roll-Up, Drill-Down, Slice, Dice, Pivot + K-Means (K=2/K=4) + Apriori & FP-Growth.',
              icon: 'query_stats',
            },
          ].map((s) => (
            <div
              key={s.step}
              className="p-3.5 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col justify-between gap-2"
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-[#175D44]">{s.step}</span>
                <span className="material-symbols-outlined text-[#175D44] text-[18px]">
                  {s.icon}
                </span>
              </div>
              <div>
                <h4 className="font-headline font-semibold text-xs text-[#0F1F18] mb-1">
                  {s.title}
                </h4>
                <p className="text-[11px] text-[#404943] leading-relaxed">{s.detail}</p>
              </div>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  )
}
