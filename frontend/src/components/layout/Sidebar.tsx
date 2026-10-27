import React from 'react'
import { AppIcon } from '../common/AppIcon'

export type PageId =
  | 'overview'
  | 'dataset-explorer'
  | 'data-quality-etl'
  | 'data-warehouse'
  | 'olap-analytics'
  | 'visual-pattern-mining'
  | 'association-rules'
  | 'image-analysis'
  | 'reports-methodology'

interface SidebarProps {
  activePage: PageId
  setActivePage: (page: PageId) => void
  isMobileOpen: boolean
  setIsMobileOpen: (open: boolean) => void
}

const NAV_ITEMS: Array<{ id: PageId; label: string; icon: string }> = [
  { id: 'overview', label: 'Overview', icon: 'dashboard' },
  { id: 'dataset-explorer', label: 'Dataset Explorer', icon: 'travel_explore' },
  { id: 'image-analysis', label: 'Image Analysis', icon: 'biotech' },
  { id: 'data-quality-etl', label: 'Data Quality & ETL', icon: 'rule' },
  { id: 'data-warehouse', label: 'Data Warehouse', icon: 'database' },
  { id: 'olap-analytics', label: 'OLAP Analytics', icon: 'view_in_ar' },
  { id: 'visual-pattern-mining', label: 'Visual Pattern Mining', icon: 'grain' },
  { id: 'association-rules', label: 'Association Rules', icon: 'hub' },
  { id: 'reports-methodology', label: 'Reports & Methodology', icon: 'menu_book' },
]

export const Sidebar: React.FC<SidebarProps> = ({
  activePage,
  setActivePage,
  isMobileOpen,
  setIsMobileOpen,
}) => {
  return (
    <>
      {/* Mobile backdrop */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setIsMobileOpen(false)}
        />
      )}

      <aside
        className={`fixed left-0 top-0 bottom-0 w-64 bg-[#24342D] text-[#E2F5EB] z-50 flex flex-col justify-between select-none shadow-[0_1px_8px_rgba(0,0,0,0.12)] transition-transform duration-300 lg:translate-x-0 ${
          isMobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col">
          {/* Logo & Platform Title */}
          <div className="px-4 pt-6 pb-4 border-b border-[#D4E7DC]/10">
            <div className="flex items-center gap-2 mb-1">
              <div className="w-8 h-8 rounded-lg bg-[#34765B] flex items-center justify-center shrink-0 shadow-inner">
                <AppIcon name="potted_plant" className="text-white w-5 h-5" />
              </div>
              <div>
                <h1 className="font-headline text-lg font-semibold tracking-tight text-white leading-none">
                  AgroVision-Mine
                </h1>
                <span className="font-mono text-[10px] text-[#ADF1D0] block uppercase tracking-wider mt-0.5 font-medium">
                  Intelligence Platform
                </span>
              </div>
            </div>
            <p className="text-xs text-[#E2F5EB]/70 leading-tight mt-1.5">
              Multimodal Data Warehouse & Pattern Mining
            </p>
          </div>

          {/* Navigation Section */}
          <div className="px-4 pt-4 pb-2">
            <span className="font-mono text-[10px] text-[#E2F5EB]/50 tracking-wider uppercase font-semibold">
              Platform Navigation
            </span>
          </div>

          <nav className="flex flex-col gap-1 px-2">
            {NAV_ITEMS.map((item) => {
              const isActive = activePage === item.id
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActivePage(item.id)
                    setIsMobileOpen(false)
                  }}
                  className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-left transition-colors text-xs font-medium ${
                    isActive
                      ? 'bg-[#34765B] text-white shadow-sm font-semibold'
                      : 'text-[#E2F5EB]/80 hover:bg-[#34765B]/30 hover:text-white'
                  }`}
                >
                  <AppIcon
                    name={item.icon}
                    className={`w-4 h-4 shrink-0 ${
                      isActive ? 'text-white' : 'text-[#ADF1D0]/80'
                    }`}
                  />
                  <span>{item.label}</span>
                </button>
              )
            })}
          </nav>
        </div>

        {/* Footer: Verified Dataset Pill */}
        <div className="p-4 border-t border-[#D4E7DC]/10">
          <div className="bg-[#D4E7DC]/10 rounded-xl p-3 flex flex-col gap-1.5">
            <div className="flex items-center justify-between">
              <span className="font-mono text-[10px] text-[#FFDEA7] font-semibold uppercase tracking-wider">
                Frozen Dataset v2
              </span>
              <span className="inline-flex items-center px-1.5 py-0.5 rounded-full font-mono text-[9px] bg-[#C3EFAA] text-[#2B4F1C] font-bold">
                Active
              </span>
            </div>
            <div className="flex items-center gap-1.5 text-[#E2F5EB]/80 text-[11px]">
              <AppIcon name="verified" className="text-[#C3EFAA] w-3.5 h-3.5 shrink-0" />
              <span className="font-mono text-[10px]">SHA-256 verified</span>
            </div>
            <div className="font-mono text-[9px] text-[#E2F5EB]/50 truncate">
              chk: c7fd16dcd6c1f862...
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
