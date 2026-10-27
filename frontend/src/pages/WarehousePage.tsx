import React, { useEffect, useState } from 'react'
import { api } from '../services/api'
import type { WarehouseSchemaResponse, TableInfo } from '../types/api'
import { SectionCard } from '../components/common/SectionCard'
import { KPICard } from '../components/common/KPICard'
import { AppIcon } from '../components/common/AppIcon'

export const WarehousePage: React.FC = () => {
  const [data, setData] = useState<WarehouseSchemaResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedTable, setSelectedTable] = useState<string>('disease_observation_fact')

  useEffect(() => {
    api
      .getWarehouseSchema()
      .then((res) => {
        setData(res)
        setLoading(false)
      })
      .catch((err) => {
        console.error('Failed to load warehouse schema:', err)
        setLoading(false)
      })
  }, [])

  if (loading || !data) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-3 text-[#404943]">
        <AppIcon name="progress_activity" className="text-4xl animate-spin text-[#175D44]" />
        <span className="text-sm font-mono">Connecting to SQLite Star Schema warehouse...</span>
      </div>
    )
  }

  const currentTable: TableInfo | undefined = data.tables.find(
    (t) => t.table_name === selectedTable
  )

  return (
    <div className="flex flex-col gap-6 max-w-[1720px] mx-auto w-full pb-12">
      {/* Top Banner */}
      <section className="bg-white rounded-2xl p-6 border border-[#E2E7DF] shadow-xs flex flex-col gap-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#E0F2E8] text-[#175D44] flex items-center justify-center">
              <AppIcon name="database" className="text-[24px]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-headline text-xl font-bold text-[#0F1F18]">
                  AgroVision-Mine Star Schema Data Warehouse
                </h1>
                <span className="px-2 py-0.5 rounded-full font-mono text-[10px] bg-[#E0F2E8] text-[#175D44] font-bold">
                  SQLite 3 Relational
                </span>
              </div>
              <p className="text-xs text-[#404943]">
                Dimensional modeling with 4 dimension tables, 1 central fact table, and strict foreign-key integrity
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-[#F7F6EF] border border-[#E2E7DF] text-[#175D44] font-mono text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-[#175D44]"></span>
              PRAGMA foreign_keys = ON
            </span>
          </div>
        </div>
      </section>

      {/* KPI Cards: Warehouse Grain and Dimensions */}
      <section className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <KPICard
          label="Fact Table Grain"
          value="1 Specimen"
          unit="Observation"
          icon="center_focus_strong"
          iconColor="text-[#175D44]"
          progressLabel="disease_observation_fact"
          progressPercent={100}
          footerNote="Single leaf image observation"
        />

        <KPICard
          label="Dimension Tables"
          value="4"
          unit="Tables"
          icon="account_tree"
          iconColor="text-[#426831]"
          progressLabel="Crop • Disease • Image • Visual"
          progressPercent={100}
          footerNote="Surrogate primary keys enforced"
        />

        <KPICard
          label="Dimensional Measures"
          value="5"
          unit="Aggregated"
          icon="analytics"
          iconColor="text-[#6C4C00]"
          progressLabel="Severity, Sharpness, Contrast, etc."
          progressPercent={100}
          footerNote="Additive and semi-additive metrics"
        />

        <KPICard
          label="Warehouse DB File"
          value="118.8 KB"
          icon="folder_zip"
          iconColor="text-[#175D44]"
          progressLabel="database/agrovision_warehouse.db"
          progressPercent={100}
          footerNote="ACID compliant transactional storage"
        />
      </section>

      {/* Star Schema Interactive Topology Diagram */}
      <SectionCard
        moduleNumber="Dimensional Topology"
        title="Star Schema Relational Architecture"
        subtitle="Visual representation of dimension-to-fact relationships and foreign-key dependencies"
      >
        <div className="p-6 bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] flex flex-col items-center justify-center">
          <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
            {/* Left Dimensions */}
            <div className="flex flex-col gap-4">
              <div
                onClick={() => setSelectedTable('dim_crop')}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                  selectedTable === 'dim_crop'
                    ? 'bg-[#175D44] text-white border-[#175D44] shadow-md'
                    : 'bg-white border-[#E2E7DF] hover:border-[#175D44]'
                }`}
              >
                <div className="flex items-center justify-between font-mono text-xs font-bold mb-1">
                  <span>dim_crop</span>
                  <span className="text-[10px] opacity-80">PK: crop_key</span>
                </div>
                <p className="text-[11px] opacity-90 leading-tight">
                  Taxonomic hierarchy: Crop Category &gt; Crop Name &gt; Genus
                </p>
              </div>

              <div
                onClick={() => setSelectedTable('dim_disease')}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                  selectedTable === 'dim_disease'
                    ? 'bg-[#175D44] text-white border-[#175D44] shadow-md'
                    : 'bg-white border-[#E2E7DF] hover:border-[#175D44]'
                }`}
              >
                <div className="flex items-center justify-between font-mono text-xs font-bold mb-1">
                  <span>dim_disease</span>
                  <span className="text-[10px] opacity-80">PK: disease_key</span>
                </div>
                <p className="text-[11px] opacity-90 leading-tight">
                  Etiology hierarchy: Pathogen Type &gt; Disease Name &gt; Agent
                </p>
              </div>
            </div>

            {/* Central Fact Table */}
            <div
              onClick={() => setSelectedTable('disease_observation_fact')}
              className={`p-5 rounded-2xl border-2 transition-all cursor-pointer text-center flex flex-col items-center gap-2 ${
                selectedTable === 'disease_observation_fact'
                  ? 'bg-[#175D44] text-white border-[#175D44] shadow-xl'
                  : 'bg-white border-[#34765B] hover:shadow-lg'
              }`}
            >
              <div className="w-10 h-10 rounded-full bg-[#E0F2E8] text-[#175D44] flex items-center justify-center">
                <AppIcon name="hub" className="text-[20px]" />
              </div>
              <h3 className="font-headline font-bold text-sm">disease_observation_fact</h3>
              <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-black/10">
                Central Observation Fact Table
              </span>
              <div className="text-[11px] opacity-90 mt-1 space-y-0.5 font-mono">
                <div>FK: crop_key, disease_key</div>
                <div>FK: image_key, feature_key</div>
                <div className="pt-1 text-[#C3EFAA] font-bold">Measures: Severity, Sharpness</div>
              </div>
            </div>

            {/* Right Dimensions */}
            <div className="flex flex-col gap-4">
              <div
                onClick={() => setSelectedTable('dim_image')}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                  selectedTable === 'dim_image'
                    ? 'bg-[#175D44] text-white border-[#175D44] shadow-md'
                    : 'bg-white border-[#E2E7DF] hover:border-[#175D44]'
                }`}
              >
                <div className="flex items-center justify-between font-mono text-xs font-bold mb-1">
                  <span>dim_image</span>
                  <span className="text-[10px] opacity-80">PK: image_key</span>
                </div>
                <p className="text-[11px] opacity-90 leading-tight">
                  Raster metadata: File Path, Dataset Source, SHA-256
                </p>
              </div>

              <div
                onClick={() => setSelectedTable('dim_visual_feature')}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                  selectedTable === 'dim_visual_feature'
                    ? 'bg-[#175D44] text-white border-[#175D44] shadow-md'
                    : 'bg-white border-[#E2E7DF] hover:border-[#175D44]'
                }`}
              >
                <div className="flex items-center justify-between font-mono text-xs font-bold mb-1">
                  <span>dim_visual_feature</span>
                  <span className="text-[10px] opacity-80">PK: feature_key</span>
                </div>
                <p className="text-[11px] opacity-90 leading-tight">
                  Continuous descriptors: RGB, GLCM Texture, Dominant Tone
                </p>
              </div>
            </div>
          </div>
        </div>
      </SectionCard>

      {/* Live Table Inspector */}
      <SectionCard
        moduleNumber="Table DDL & Schema Inspector"
        title={`Table: ${selectedTable}`}
        subtitle={`Live SQLite column schema, data types, constraints, and row count (${currentTable?.row_count ?? 0} rows)`}
        actions={
          <div className="flex items-center gap-1.5 p-1 rounded-lg bg-[#F7F6EF] border border-[#E2E7DF]">
            {data.tables.map((t) => (
              <button
                key={t.table_name}
                onClick={() => setSelectedTable(t.table_name)}
                className={`px-2.5 py-1 rounded text-xs font-mono transition-colors ${
                  selectedTable === t.table_name
                    ? 'bg-[#175D44] text-white font-bold'
                    : 'text-[#404943] hover:text-[#0F1F18]'
                }`}
              >
                {t.table_name}
              </button>
            ))}
          </div>
        }
      >
        <div className="border border-[#E2E7DF] rounded-xl overflow-hidden bg-white">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="bg-[#E5F8ED] text-[#175D44] font-mono text-[11px] border-b border-[#E2E7DF]">
              <tr>
                <th className="py-2.5 px-4 font-semibold">Column ID</th>
                <th className="py-2.5 px-4 font-semibold">Column Name</th>
                <th className="py-2.5 px-4 font-semibold">SQL Type</th>
                <th className="py-2.5 px-4 font-semibold">Constraint</th>
                <th className="py-2.5 px-4 font-semibold">Not Null</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E2E7DF]">
              {currentTable?.columns.map((col) => (
                <tr key={col.cid} className="hover:bg-[#F7F6EF] transition-colors">
                  <td className="py-2.5 px-4 font-mono text-[#707973]">{col.cid}</td>
                  <td className="py-2.5 px-4 font-mono font-bold text-[#0F1F18] flex items-center gap-1.5">
                    {col.name}
                    {col.primary_key && (
                      <span className="px-1.5 py-0.2 rounded font-mono text-[9px] bg-[#C3EFAA] text-[#2B4F1C] font-bold">
                        PK
                      </span>
                    )}
                    {col.name.endsWith('_key') && !col.primary_key && (
                      <span className="px-1.5 py-0.2 rounded font-mono text-[9px] bg-[#E0F2E8] text-[#175D44] font-bold">
                        FK
                      </span>
                    )}
                  </td>
                  <td className="py-2.5 px-4 font-mono text-[#175D44] font-semibold">{col.type}</td>
                  <td className="py-2.5 px-4 text-[#404943]">
                    {col.primary_key ? 'PRIMARY KEY' : col.name.endsWith('_key') ? 'REFERENCES' : '—'}
                  </td>
                  <td className="py-2.5 px-4 font-mono">
                    {col.notnull || col.primary_key ? (
                      <span className="text-[#175D44] font-bold">YES</span>
                    ) : (
                      <span className="text-[#707973]">NULLABLE</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SectionCard>
    </div>
  )
}
