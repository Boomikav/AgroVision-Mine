import React, { useEffect, useState } from 'react'
import { api } from '../services/api'
import { SectionCard } from '../components/common/SectionCard'

export const ReportsMethodologyPage: React.FC = () => {
  const [catalog, setCatalog] = useState<any | null>(null)
  const [activeReportId, setActiveReportId] = useState<string>('review2_evaluation')
  const [reportContent, setReportContent] = useState<any | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    api
      .getReportsCatalog()
      .then((res) => {
        setCatalog(res)
        loadReport('review2_evaluation')
      })
      .catch((err) => {
        console.error('Failed to load reports catalog:', err)
      })
  }, [])

  const loadReport = (id: string) => {
    setActiveReportId(id)
    setLoading(true)
    api
      .getReportContent(id)
      .then((res) => {
        setReportContent(res)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load report content:', err)
        setLoading(false)
      })
  }

  const handleDownload = () => {
    if (!reportContent) return
    const blob = new Blob([JSON.stringify(reportContent, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${activeReportId}_v2.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="flex flex-col gap-6 max-w-[1720px] mx-auto w-full pb-12">
      {/* Top Banner */}
      <section className="bg-white rounded-2xl p-6 border border-[#E2E7DF] shadow-xs flex flex-col gap-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#E0F2E8] text-[#175D44] flex items-center justify-center">
              <span className="material-symbols-outlined text-[24px]">menu_book</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-headline text-xl font-bold text-[#0F1F18]">
                  Academic Methodology & Verified Evaluation Reports
                </h1>
                <span className="px-2 py-0.5 rounded-full font-mono text-[10px] bg-[#E0F2E8] text-[#175D44] font-bold">
                  Peer-Review Ready
                </span>
              </div>
              <p className="text-xs text-[#404943]">
                Full computational audit reports, scientific methodology, experimental caveats, and raw artifacts
              </p>
            </div>
          </div>
        </div>

        {/* Report Selector Pills */}
        <div className="flex flex-wrap items-center gap-2 pt-3 border-t border-[#E2E7DF]">
          {catalog?.available_reports.map((rep: any) => (
            <button
              key={rep.id}
              onClick={() => loadReport(rep.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                activeReportId === rep.id
                  ? 'bg-[#175D44] text-white shadow-xs'
                  : 'bg-[#F7F6EF] text-[#404943] hover:text-[#0F1F18] border border-[#E2E7DF]'
              }`}
            >
              <span>{rep.title}</span>
            </button>
          ))}
        </div>
      </section>

      {/* Scientific Caveats & Research Limitations Card */}
      <SectionCard
        moduleNumber="Academic Ethics & Epistemology"
        title="Scientific Boundaries & Research Disclaimers"
        subtitle="Mandatory academic guidelines governing interpretability and model limitations"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-xs pt-1">
          <div className="p-4 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2">
            <div className="flex items-center gap-2 text-[#175D44] font-semibold">
              <span className="material-symbols-outlined text-[18px]">bubble_chart</span>
              <span>K=2 Metric-Supported Solution</span>
            </div>
            <p className="text-[#404943] leading-relaxed">
              Silhouette (0.4060) and Davies-Bouldin (1.0990) confirm K=2 as the primary mathematical grouping. K=4 represents an exploratory sub-partition with higher intra-cluster dispersion (Silhouette 0.1651).
            </p>
          </div>

          <div className="p-4 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2">
            <div className="flex items-center gap-2 text-[#6C4C00] font-semibold">
              <span className="material-symbols-outlined text-[18px]">hub</span>
              <span>Association Does Not Prove Causality</span>
            </div>
            <p className="text-[#404943] leading-relaxed">
              High lift values establish statistical co-occurrence across spatial texture and color moments. They do not constitute biochemical or pathological causation.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2">
            <div className="flex items-center gap-2 text-[#BA1A1A] font-semibold">
              <span className="material-symbols-outlined text-[18px]">warning</span>
              <span>No Autonomous Clinical Diagnosis</span>
            </div>
            <p className="text-[#404943] leading-relaxed">
              Unsupervised clusters isolate visual descriptor distributions. Clusters must never be presented as autonomous or automated disease diagnostic systems.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2">
            <div className="flex items-center gap-2 text-[#404943] font-semibold">
              <span className="material-symbols-outlined text-[18px]">pie_chart</span>
              <span>Dataset Provenance Imbalance</span>
            </div>
            <p className="text-[#404943] leading-relaxed">
              PlantDoc is the dominant source (2,560 images, 98.6%) compared to ICAR/OGD (36 images, 1.4%). Rice specimens are exclusively derived from ICAR macro photographs.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2">
            <div className="flex items-center gap-2 text-[#404943] font-semibold">
              <span className="material-symbols-outlined text-[18px]">bug_report</span>
              <span>Pest Symptom Underrepresentation</span>
            </div>
            <p className="text-[#404943] leading-relaxed">
              Pest signs represent a minority class (2 specimens, Spider Mite in tomato). Findings primarily reflect fungal and bacterial foliar lesions.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2">
            <div className="flex items-center gap-2 text-[#175D44] font-semibold">
              <span className="material-symbols-outlined text-[18px]">verified</span>
              <span>100% Cryptographic Reproducibility</span>
            </div>
            <p className="text-[#404943] leading-relaxed">
              All 2,596 manifest records and 44-column feature store files remain frozen and verified via SHA-256 hashes against accidental modification.
            </p>
          </div>
        </div>
      </SectionCard>

      {/* Report Raw JSON Viewer & Download */}
      <SectionCard
        moduleNumber="Artifact Inspector"
        title={`Verified Report: ${activeReportId}`}
        subtitle="Cryptographically backed raw JSON evaluation artifact loaded from data/reports/"
        actions={
          <button
            onClick={handleDownload}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#175D44] text-white hover:bg-[#34765B] text-xs font-semibold transition-colors shadow-xs"
          >
            <span className="material-symbols-outlined text-[16px]">download</span>
            <span>Download JSON</span>
          </button>
        }
      >
        {loading ? (
          <div className="flex items-center justify-center py-16 gap-2 text-xs text-[#404943]">
            <span className="material-symbols-outlined animate-spin text-[18px]">progress_activity</span>
            <span>Loading evaluation artifact...</span>
          </div>
        ) : (
          <div className="bg-[#1E1E1E] rounded-xl p-4 text-[#D4D4D4] font-mono text-xs overflow-x-auto max-h-[500px] border border-[#333333]">
            <pre className="whitespace-pre-wrap leading-relaxed text-[#9CDCFE]">
              {JSON.stringify(reportContent, null, 2)}
            </pre>
          </div>
        )}
      </SectionCard>
    </div>
  )
}
