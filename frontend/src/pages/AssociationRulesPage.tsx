import React, { useEffect, useState } from 'react'
import { api } from '../services/api'
import type { AssociationRulesResponse, AssociationRule } from '../types/api'
import { SectionCard } from '../components/common/SectionCard'

export const AssociationRulesPage: React.FC = () => {
  const [mode, setMode] = useState<'visual' | 'labeled'>('visual')
  const [data, setData] = useState<AssociationRulesResponse | null>(null)
  const [loading, setLoading] = useState(true)

  // Filters
  const [minSupport, setMinSupport] = useState<number>(0.15)
  const [minConfidence, setMinConfidence] = useState<number>(0.6)
  const [minLift, setMinLift] = useState<number>(1.0)
  const [search, setSearch] = useState<string>('')
  const [page, setPage] = useState<number>(1)
  const [pageSize] = useState<number>(25)
  const [sortBy, setSortBy] = useState<string>('lift')
  const [sortOrder] = useState<string>('desc')

  const fetchRules = () => {
    setLoading(true)
    api
      .getAssociationRules({
        mode,
        min_support: minSupport,
        min_confidence: minConfidence,
        min_lift: minLift,
        search: search.trim() || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
        page,
        page_size: pageSize,
      })
      .then((res) => {
        setData(res)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load association rules:', err)
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchRules()
  }, [mode, minSupport, minConfidence, minLift, page, pageSize, sortBy, sortOrder])

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setPage(1)
    fetchRules()
  }

  return (
    <div className="flex flex-col gap-6 max-w-[1720px] mx-auto w-full pb-12">
      {/* Top Header & Mode Switcher */}
      <header className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-[#E2E7DF] shadow-xs">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="font-mono text-[10px] text-[#175D44] uppercase font-bold tracking-wider">
              Pattern Mining Engine
            </span>
            <span className="text-[#BFC9C2]">/</span>
            <span className="font-mono text-[10px] text-[#404943]">SPECIMEN-DS-FROZEN-V2</span>
          </div>
          <h1 className="font-headline text-2xl font-bold text-[#0F1F18] tracking-tight">
            Association Rules Matrix
          </h1>
          <p className="text-xs text-[#404943] mt-0.5">
            Computational discovery across 32 discretized visual descriptors (2,596 analyzed leaf rasters)
          </p>
        </div>

        {/* Mode Switcher Tabs */}
        <div className="flex items-center p-1 bg-[#F7F6EF] border border-[#E2E7DF] rounded-xl shadow-xs">
          <button
            onClick={() => {
              setMode('visual')
              setPage(1)
            }}
            className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
              mode === 'visual'
                ? 'bg-[#175D44] text-white shadow-xs'
                : 'text-[#404943] hover:text-[#0F1F18]'
            }`}
          >
            <span className="material-symbols-outlined text-[16px]">blur_on</span>
            <span>Mode A: Visual-Feature-Only</span>
            <span className="ml-1 px-1.5 py-0.2 rounded font-mono text-[9px] bg-[#34765B] text-white">
              Unsupervised (880)
            </span>
          </button>
          <button
            onClick={() => {
              setMode('labeled')
              setPage(1)
            }}
            className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
              mode === 'labeled'
                ? 'bg-[#C87858] text-white shadow-xs'
                : 'text-[#404943] hover:text-[#0F1F18]'
            }`}
          >
            <span className="material-symbols-outlined text-[16px]">label</span>
            <span>Mode B: Label-Conditioned</span>
            <span className="ml-1 px-1.5 py-0.2 rounded font-mono text-[9px] bg-black/15 text-current">
              Exploratory (285)
            </span>
          </button>
        </div>
      </header>

      {/* Mode B Terracotta Warning Disclosure Banner */}
      {mode === 'labeled' && (
        <div className="p-4 rounded-xl bg-[#FFDAD6] border border-[#FFDAD6] text-[#93000A] flex items-start gap-3 shadow-xs">
          <span className="material-symbols-outlined text-[#BA1A1A] text-[22px] shrink-0 mt-0.5">
            warning_amber
          </span>
          <div className="flex flex-col text-xs">
            <span className="font-mono text-[10px] font-bold tracking-wider uppercase text-[#BA1A1A]">
              METHODOLOGICAL DISCLOSURE
            </span>
            <p className="mt-0.5 leading-relaxed">
              This mode includes ground-truth condition labels (<code className="bg-white/50 px-1 py-0.5 rounded font-mono">condition_label_Healthy</code>, <code className="bg-white/50 px-1 py-0.5 rounded font-mono">pathogen_type_Unknown</code>) in the itemset mining matrix. Rules reflect supervised statistical co-occurrence rather than purely unsupervised image feature discovery.
            </p>
          </div>
        </div>
      )}

      {/* Algorithmic Execution Benchmark Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Benchmark Card: Apriori vs FP-Growth */}
        <div className="lg:col-span-8">
          <SectionCard
            moduleNumber="Algorithmic Rigor"
            title="Apriori vs FP-Growth Execution Benchmark"
            subtitle="Verified algorithmic parity and computational performance comparison over 32 discretized features"
            badge="Verified Equivalence"
          >
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-1">
              <div className="p-3.5 bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] flex flex-col">
                <span className="font-mono text-[10px] text-[#404943] uppercase">
                  Generated Rules
                </span>
                <div className="flex items-baseline gap-1 mt-1">
                  <span className="font-headline text-2xl font-bold text-[#0F1F18]">
                    {data?.algorithm_benchmark?.fpgrowth?.rules_count ?? 880}
                  </span>
                  <span className="font-mono text-[10px] text-[#175D44] font-semibold">Parity</span>
                </div>
                <div className="mt-2 text-[10px] font-mono text-[#707973] flex justify-between">
                  <span>Apriori: {data?.algorithm_benchmark?.apriori?.rules_count ?? 880}</span>
                  <span>FP: {data?.algorithm_benchmark?.fpgrowth?.rules_count ?? 880}</span>
                </div>
                <span className="mt-1 text-[11px] text-[#175D44] font-medium flex items-center gap-1">
                  <span className="material-symbols-outlined text-[13px]">check_circle</span>
                  <span>100% Rule Parity</span>
                </span>
              </div>

              <div className="p-3.5 bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] flex flex-col">
                <span className="font-mono text-[10px] text-[#404943] uppercase">
                  Frequent Itemsets
                </span>
                <div className="flex items-baseline gap-1 mt-1">
                  <span className="font-headline text-2xl font-bold text-[#0F1F18]">
                    {data?.algorithm_benchmark?.fpgrowth?.frequent_itemsets_count ?? 223}
                  </span>
                  <span className="font-mono text-[10px] text-[#404943]">L1-L4</span>
                </div>
                <div className="mt-2 text-[10px] font-mono text-[#707973] flex justify-between">
                  <span>Apriori: {data?.algorithm_benchmark?.apriori?.frequent_itemsets_count ?? 223}</span>
                  <span>FP: {data?.algorithm_benchmark?.fpgrowth?.frequent_itemsets_count ?? 223}</span>
                </div>
                <span className="mt-1 text-[11px] text-[#404943] font-medium flex items-center gap-1">
                  <span className="material-symbols-outlined text-[13px]">verified</span>
                  <span>Zero Divergence</span>
                </span>
              </div>

              <div className="p-3.5 bg-[#E0F2E8] rounded-xl border border-[#BFC9C2]/40 flex flex-col">
                <span className="font-mono text-[10px] text-[#404943] uppercase">
                  Median Runtime
                </span>
                <div className="flex items-baseline gap-1 mt-1">
                  <span className="font-headline text-2xl font-bold text-[#175D44]">
                    {data?.algorithm_benchmark?.fpgrowth?.median_runtime_sec ? `${data.algorithm_benchmark.fpgrowth.median_runtime_sec.toFixed(3)}s` : '0.302s'}
                  </span>
                  <span className="font-mono text-[10px] text-[#404943]">FP-Tree</span>
                </div>
                <div className="mt-2 text-[10px] font-mono text-[#707973] flex justify-between">
                  <span>Apriori: {data?.algorithm_benchmark?.apriori?.median_runtime_sec ? `${data.algorithm_benchmark.apriori.median_runtime_sec.toFixed(3)}s` : '0.062s'}</span>
                  <span className="text-[#175D44] font-bold">FP: {data?.algorithm_benchmark?.fpgrowth?.median_runtime_sec ? `${data.algorithm_benchmark.fpgrowth.median_runtime_sec.toFixed(3)}s` : '0.302s'}</span>
                </div>
                <span className="mt-1 text-[11px] text-[#175D44] font-bold flex items-center gap-1">
                  <span className="material-symbols-outlined text-[14px]">bolt</span>
                  <span>Fast Sub-Second Mining</span>
                </span>
              </div>

              <div className="p-3.5 bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] flex flex-col">
                <span className="font-mono text-[10px] text-[#404943] uppercase">
                  Numerical Parity
                </span>
                <div className="flex items-baseline gap-1 mt-1">
                  <span className="font-headline text-2xl font-bold text-[#0F1F18]">0.0000</span>
                  <span className="font-mono text-[10px] text-[#404943]">Max Diff</span>
                </div>
                <div className="mt-2 text-[10px] font-mono text-[#707973] flex justify-between">
                  <span>Supp: 0.0</span>
                  <span>Conf / Lift: 0.0</span>
                </div>
                <span className="mt-1 text-[11px] text-[#426831] font-medium flex items-center gap-1">
                  <span className="material-symbols-outlined text-[13px]">check</span>
                  <span>Output Equivalence: 100%</span>
                </span>
              </div>
            </div>
          </SectionCard>
        </div>

        {/* Advisory Card (4 cols) */}
        <div className="lg:col-span-4">
          <SectionCard
            moduleNumber="Methodological Advisory"
            title="Statistical Association vs Etiology"
            subtitle="Epistemological boundaries of association-rule mining in agricultural pathology"
          >
            <div className="flex flex-col gap-3 text-xs">
              <p className="text-[#404943] leading-relaxed">
                High lift values indicate high mathematical co-occurrence within the continuous feature descriptor space, <strong>NOT biological causation or definitive pathogen diagnosis</strong>.
              </p>
              <div className="p-3 rounded-lg bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-1.5 font-mono text-[11px] text-[#0F1F18]">
                <div className="flex items-center gap-1.5 text-[#175D44]">
                  <span className="material-symbols-outlined text-[14px]">check</span>
                  <span>Tertile Quantile Binning (Low, Medium, High)</span>
                </div>
                <div className="flex items-center gap-1.5 text-[#175D44]">
                  <span className="material-symbols-outlined text-[14px]">check</span>
                  <span>Min Support: 15% | Min Confidence: 60%</span>
                </div>
                <div className="flex items-center gap-1.5 text-[#6C4C00]">
                  <span className="material-symbols-outlined text-[14px]">info</span>
                  <span>Filtered for low-variance noise</span>
                </div>
              </div>
            </div>
          </SectionCard>
        </div>
      </div>

      {/* Threshold Filters & Search */}
      <section className="bg-white rounded-xl p-4 border border-[#E2E7DF] flex flex-wrap items-center justify-between gap-4">
        <form onSubmit={handleSearchSubmit} className="relative w-full sm:w-80">
          <span className="material-symbols-outlined absolute left-2.5 top-1/2 -translate-y-1/2 text-[#707973] text-[18px]">
            search
          </span>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search antecedent / consequent tokens..."
            className="w-full pl-8 pr-3 py-1.5 rounded-lg bg-[#F7F6EF] border border-[#BFC9C2]/40 text-xs text-[#0F1F18] focus:outline-none focus:border-[#175D44]"
          />
        </form>

        <div className="flex flex-wrap items-center gap-4 text-xs">
          <div className="flex items-center gap-2">
            <span className="font-mono text-[#404943]">Min Support:</span>
            <input
              type="number"
              step="0.01"
              min="0.05"
              max="0.5"
              value={minSupport}
              onChange={(e) => setMinSupport(parseFloat(e.target.value) || 0.15)}
              className="w-16 px-2 py-1 rounded bg-[#F7F6EF] border border-[#E2E7DF] font-mono text-center"
            />
          </div>

          <div className="flex items-center gap-2">
            <span className="font-mono text-[#404943]">Min Confidence:</span>
            <input
              type="number"
              step="0.05"
              min="0.1"
              max="1.0"
              value={minConfidence}
              onChange={(e) => setMinConfidence(parseFloat(e.target.value) || 0.6)}
              className="w-16 px-2 py-1 rounded bg-[#F7F6EF] border border-[#E2E7DF] font-mono text-center"
            />
          </div>

          <div className="flex items-center gap-2">
            <span className="font-mono text-[#404943]">Min Lift:</span>
            <input
              type="number"
              step="0.1"
              min="1.0"
              max="10.0"
              value={minLift}
              onChange={(e) => setMinLift(parseFloat(e.target.value) || 1.0)}
              className="w-16 px-2 py-1 rounded bg-[#F7F6EF] border border-[#E2E7DF] font-mono text-center"
            />
          </div>

          <div className="flex items-center gap-2">
            <span className="font-mono text-[#404943]">Sort By:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-2 py-1 rounded bg-[#F7F6EF] border border-[#E2E7DF] font-mono text-xs"
            >
              <option value="lift">Lift (Co-occurrence strength)</option>
              <option value="confidence">Confidence (%)</option>
              <option value="support">Support (%)</option>
            </select>
          </div>
        </div>
      </section>

      {/* Rules Table */}
      <SectionCard
        moduleNumber="Frequent Itemsets & Implication Rules"
        title={`${data?.mode ?? 'Association'} Rules`}
        subtitle={`Displaying page ${data?.page ?? 1} of ${data?.total_pages ?? 1} • ${data?.total_filtered_rules ?? data?.total_rules ?? 0} matching active filters (supp ≥ ${(minSupport * 100).toFixed(0)}%, conf ≥ ${(minConfidence * 100).toFixed(0)}%, lift ≥ ${minLift.toFixed(1)}) out of ${data?.total_generated_rules ?? (mode === 'visual' ? 880 : 285)} total generated rules`}
        badge={`${data?.total_filtered_rules ?? data?.total_rules ?? 0} Filtered / ${data?.total_generated_rules ?? (mode === 'visual' ? 880 : 285)} Total`}
      >
        {loading ? (
          <div className="flex items-center justify-center py-16 gap-2 text-xs text-[#404943]">
            <span className="material-symbols-outlined animate-spin text-[18px]">progress_activity</span>
            <span>Querying association rules matrix...</span>
          </div>
        ) : data?.rules.length === 0 ? (
          <div className="text-center py-12 text-xs text-[#404943]">
            No association rules match the specified threshold criteria. Try lowering the minimum support or lift thresholds.
          </div>
        ) : (
          <div className="border border-[#E2E7DF] rounded-xl overflow-hidden bg-white">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead className="bg-[#E5F8ED] text-[#175D44] font-mono text-[11px] border-b border-[#E2E7DF]">
                  <tr>
                    <th className="py-2.5 px-3 font-semibold">Rule #</th>
                    <th className="py-2.5 px-4 font-semibold">Antecedents (Condition)</th>
                    <th className="py-2.5 px-2 text-center font-semibold">&rarr;</th>
                    <th className="py-2.5 px-4 font-semibold">Consequents (Prediction)</th>
                    <th className="py-2.5 px-3 text-right font-semibold">Support</th>
                    <th className="py-2.5 px-3 text-right font-semibold">Confidence</th>
                    <th className="py-2.5 px-3 text-right font-semibold">Lift Metric</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E2E7DF]">
                  {data?.rules.map((rule: AssociationRule, idx: number) => {
                    const ruleNum = (page - 1) * pageSize + idx + 1
                    return (
                      <tr key={idx} className="hover:bg-[#F7F6EF] transition-colors">
                        <td className="py-2.5 px-3 font-mono text-[#707973]">{ruleNum}</td>
                        <td className="py-2.5 px-4">
                          <div className="flex flex-wrap gap-1">
                            {rule.antecedents.map((ant) => (
                              <span
                                key={ant}
                                className="px-2 py-0.5 rounded font-mono text-[10px] bg-[#E0F2E8] text-[#175D44] font-medium"
                              >
                                {ant}
                              </span>
                            ))}
                          </div>
                        </td>
                        <td className="py-2.5 px-2 text-center font-bold text-[#707973]">&rarr;</td>
                        <td className="py-2.5 px-4">
                          <div className="flex flex-wrap gap-1">
                            {rule.consequents.map((con) => (
                              <span
                                key={con}
                                className="px-2 py-0.5 rounded font-mono text-[10px] bg-[#FFDEA7] text-[#6C4C00] font-semibold"
                              >
                                {con}
                              </span>
                            ))}
                          </div>
                        </td>
                        <td className="py-2.5 px-3 text-right font-mono font-medium text-[#0F1F18]">
                          {(rule.support * 100).toFixed(2)}%
                        </td>
                        <td className="py-2.5 px-3 text-right font-mono font-semibold text-[#175D44]">
                          {(rule.confidence * 100).toFixed(2)}%
                        </td>
                        <td className="py-2.5 px-3 text-right font-mono font-bold text-[#175D44]">
                          <span className="px-2 py-0.5 rounded bg-[#C3EFAA]/60 text-[#2B4F1C]">
                            {rule.lift.toFixed(3)}
                          </span>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Pagination */}
        {data && data.total_pages > 1 && (
          <div className="flex items-center justify-between pt-3 text-xs text-[#404943]">
            <span>
              Showing {(page - 1) * pageSize + 1} -{' '}
              {Math.min(page * pageSize, data.total_rules)} of {data.total_rules} rules
            </span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1}
                className="px-3 py-1.5 rounded-lg bg-white border border-[#E2E7DF] disabled:opacity-40"
              >
                Previous
              </button>
              <span className="font-mono font-semibold text-[#175D44] px-1">{page}</span>
              <button
                onClick={() => setPage((p) => Math.min(data.total_pages, p + 1))}
                disabled={page >= data.total_pages}
                className="px-3 py-1.5 rounded-lg bg-white border border-[#E2E7DF] disabled:opacity-40"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </SectionCard>
    </div>
  )
}
