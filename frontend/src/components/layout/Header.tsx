import React from 'react'
import type { PageId } from './Sidebar'
import { AppIcon } from '../common/AppIcon'

interface HeaderProps {
  activePage: PageId
  onMenuToggle: () => void
  recordsCount?: number
  searchQuery: string
  setSearchQuery: (query: string) => void
  onSearchSubmit?: () => void
}

const PAGE_TITLES: Record<PageId, string> = {
  'overview': 'Overview Dashboard',
  'dataset-explorer': 'Dataset Explorer',
  'data-quality-etl': 'Data Quality & Preprocessing',
  'data-warehouse': 'Star Schema Data Warehouse',
  'olap-analytics': 'Multimodal OLAP Analytics Engine',
  'visual-pattern-mining': 'Visual Pattern Mining Workspace',
  'association-rules': 'Association Rules Explorer',
  'image-analysis': 'Image Analysis & Inference Workbench',
  'reports-methodology': 'Academic Reports & Methodology',
}

export const Header: React.FC<HeaderProps> = ({
  activePage,
  onMenuToggle,
  recordsCount = 2596,
  searchQuery,
  setSearchQuery,
  onSearchSubmit,
}) => {
  return (
    <header className="fixed top-0 left-0 lg:left-64 right-0 h-16 bg-[#FFFFFF]/90 backdrop-blur-md z-30 border-b border-[#E2E7DF] shadow-[0_1px_4px_rgba(0,0,0,0.03)]">
      <div className="w-full h-16 px-4 lg:px-6 flex items-center justify-between gap-4">
        {/* Left: Mobile hamburger + Breadcrumbs */}
        <div className="flex items-center gap-3">
          <button
            onClick={onMenuToggle}
            className="lg:hidden p-1.5 rounded-lg text-[#26362F] hover:bg-[#E0F2E8] transition-colors"
            aria-label="Toggle Navigation"
          >
            <AppIcon name="menu" className="w-5 h-5" />
          </button>

          <div className="flex items-center gap-1.5 text-xs text-[#404943]">
            <span className="font-semibold text-[#0F1F18] hidden sm:inline">AgroVision-Mine</span>
            <span className="hidden sm:inline">
              <AppIcon name="chevron_right" className="w-3.5 h-3.5 text-[#707973]" />
            </span>
            <span className="text-[#175D44] font-medium">{PAGE_TITLES[activePage]}</span>
          </div>

          <div className="hidden md:flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-[#E0F2E8] text-[#175D44] font-mono text-[10px] border border-[#BFC9C2]/30">
            <span className="w-1.5 h-1.5 rounded-full bg-[#175D44]"></span>
            <span>v2.0-frozen ({recordsCount.toLocaleString()} records)</span>
          </div>
        </div>

        {/* Right: Search + Specimen Node metadata */}
        <div className="flex items-center gap-3">
          <div className="relative w-44 sm:w-64 md:w-72">
            <div className="absolute left-2.5 top-1/2 -translate-y-1/2 text-[#707973]">
              <AppIcon name="search" className="w-4 h-4" />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && onSearchSubmit && onSearchSubmit()}
              placeholder="Search specimens, diseases, features..."
              className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-[#E5F8ED]/60 border border-[#BFC9C2]/40 text-xs text-[#0F1F18] placeholder:text-[#404943]/60 focus:outline-none focus:border-[#175D44] focus:bg-white transition-colors"
            />
          </div>

          <div className="hidden xl:flex flex-col text-right">
            <span className="font-mono text-[11px] font-semibold text-[#0F1F18]">
              Academic Node: CSI3010
            </span>
            <span className="font-mono text-[9px] text-[#404943]">
              Warehouse: SQLite 3 | Multimodal
            </span>
          </div>

          <div className="w-8 h-8 rounded-full bg-[#34765B]/15 border border-[#34765B]/30 flex items-center justify-center text-[#175D44]">
            <AppIcon name="eco" className="w-4 h-4" />
          </div>
        </div>
      </div>
    </header>
  )
}
