import { useState } from 'react'
import { Sidebar, type PageId } from './components/layout/Sidebar'
import { Header } from './components/layout/Header'
import { OverviewPage } from './pages/OverviewPage'
import { DatasetExplorerPage } from './pages/DatasetExplorerPage'
import { DataQualityPage } from './pages/DataQualityPage'
import { WarehousePage } from './pages/WarehousePage'
import { OLAPAnalyticsPage } from './pages/OLAPAnalyticsPage'
import { VisualPatternMiningPage } from './pages/VisualPatternMiningPage'
import { AssociationRulesPage } from './pages/AssociationRulesPage'
import { ReportsMethodologyPage } from './pages/ReportsMethodologyPage'
import { ImageAnalysisPage } from './pages/ImageAnalysisPage'

export function App() {
  const [activePage, setActivePage] = useState<PageId>('overview')
  const [isMobileOpen, setIsMobileOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  const handleSearchSubmit = () => {
    if (searchQuery.trim()) {
      setActivePage('dataset-explorer')
    }
  }

  const handleNavigateToSpecimen = (imageId: string) => {
    setSearchQuery(imageId)
    setActivePage('dataset-explorer')
  }

  return (
    <div className="min-h-screen bg-[#F7F6EF] text-[#0F1F18] flex">
      {/* Persistent Left Operational Sidebar */}
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
        isMobileOpen={isMobileOpen}
        setIsMobileOpen={setIsMobileOpen}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 lg:pl-64">
        {/* Top Header */}
        <Header
          activePage={activePage}
          onMenuToggle={() => setIsMobileOpen((prev) => !prev)}
          recordsCount={2596}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          onSearchSubmit={handleSearchSubmit}
        />

        {/* Page Content Viewport */}
        <main className="flex-1 pt-20 px-4 sm:px-6 lg:px-8">
          {activePage === 'overview' && (
            <OverviewPage onNavigate={(page) => setActivePage(page)} />
          )}
          {activePage === 'dataset-explorer' && (
            <DatasetExplorerPage initialSearch={searchQuery} />
          )}
          {activePage === 'image-analysis' && (
            <ImageAnalysisPage onNavigateToSpecimen={handleNavigateToSpecimen} />
          )}
          {activePage === 'data-quality-etl' && <DataQualityPage />}
          {activePage === 'data-warehouse' && <WarehousePage />}
          {activePage === 'olap-analytics' && <OLAPAnalyticsPage />}
          {activePage === 'visual-pattern-mining' && <VisualPatternMiningPage />}
          {activePage === 'association-rules' && <AssociationRulesPage />}
          {activePage === 'reports-methodology' && <ReportsMethodologyPage />}
        </main>
      </div>
    </div>
  )
}

export default App
