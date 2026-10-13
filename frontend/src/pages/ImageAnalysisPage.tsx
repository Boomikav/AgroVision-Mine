import React, { useState, useRef } from 'react'
import { api } from '../services/api'
import type { ImageAnalysisResponse, NearestSpecimen } from '../types/api'
import { SectionCard } from '../components/common/SectionCard'
import { SpecimenModal } from '../components/common/SpecimenModal'

interface ImageAnalysisPageProps {
  onNavigateToSpecimen?: (imageId: string) => void
}

export const ImageAnalysisPage: React.FC<ImageAnalysisPageProps> = ({ onNavigateToSpecimen }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [analysisResult, setAnalysisResult] = useState<ImageAnalysisResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [activeFeatureTab, setActiveFeatureTab] = useState<'color' | 'texture' | 'shape'>('color')
  const [featureScaleMode, setFeatureScaleMode] = useState<'standardized' | 'raw'>('standardized')
  const [modalSpecimenId, setModalSpecimenId] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      selectFile(file)
    }
  }

  const selectFile = (file: File) => {
    setError(null)
    setAnalysisResult(null)

    // Validate extension
    const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
    if (!['.jpg', '.jpeg', '.png'].includes(ext)) {
      setError(`Unsupported file format '${ext}'. Please upload a JPG, JPEG, or PNG image.`)
      setSelectedFile(null)
      setPreviewUrl(null)
      return
    }

    // Validate size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      setError(`File size (${(file.size / 1024 / 1024).toFixed(2)} MB) exceeds 10 MB limit.`)
      setSelectedFile(null)
      setPreviewUrl(null)
      return
    }

    setSelectedFile(file)
    const url = URL.createObjectURL(file)
    setPreviewUrl(url)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      selectFile(e.dataTransfer.files[0])
    }
  }

  const handleAnalyze = async () => {
    if (!selectedFile) return
    setLoading(true)
    setError(null)

    try {
      const res = await api.analyzeImage(selectedFile)
      setAnalysisResult(res)
    } catch (err: any) {
      setError(err.message || 'Image analysis failed. Please verify file integrity.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setSelectedFile(null)
    setPreviewUrl(null)
    setAnalysisResult(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="flex flex-col gap-6 max-w-[1720px] mx-auto w-full pb-16">
      {/* Top Banner & Context */}
      <header className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-[#E2E7DF] shadow-xs">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="font-mono text-[10px] text-[#175D44] uppercase font-bold tracking-wider">
              Diagnostic Preprocessing & Inference
            </span>
            <span className="text-[#BFC9C2]">/</span>
            <span className="font-mono text-[10px] text-[#404943]">STANDARDIZED DESCRIPTOR PIPELINE</span>
          </div>
          <h1 className="font-headline text-2xl font-bold text-[#0F1F18] tracking-tight">
            Visual Specimen Analysis Workbench
          </h1>
          <p className="text-xs text-[#404943] mt-0.5">
            Extracts 32 continuous visual descriptors, projects into calibrated latent space, and retrieves nearest frozen reference specimens.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-[#E0F2E8] text-[#175D44] font-mono text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-[#175D44]"></span>
            <span>Zero-Mutation In-Memory Sandbox</span>
          </span>
        </div>
      </header>

      {/* Mandatory Scientific Boundary & Ethics Disclosure Alert */}
      <div className="p-4 rounded-xl bg-[#FFF8E1] border border-[#FFE082] text-[#5D4037] flex items-start gap-3 shadow-xs">
        <span className="material-symbols-outlined text-[#F57F17] text-[24px] shrink-0 mt-0.5">
          verified_user
        </span>
        <div className="flex flex-col text-xs">
          <span className="font-mono text-[10px] font-bold tracking-wider uppercase text-[#E65100]">
            ACADEMIC BOUNDARIES & EPISTEMOLOGICAL NOTICE
          </span>
          <p className="mt-1 leading-relaxed text-[#4E342E]">
            <strong>Supervised disease classification is NOT implemented or validated in this system.</strong> Visual proximity (Euclidean distance across 32 normalized color, GLCM texture, and contour descriptors) and unsupervised $K$-Means clustering reflect mathematical morphology, <strong>NOT biological infection certainty, medical diagnosis, or etiology</strong>. Uploaded specimens are evaluated ephemerally in-memory and will never mutate the frozen canonical warehouse.
          </p>
        </div>
      </div>

      {/* Upload & Inspection Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Upload & Preview Card (5 cols) */}
        <div className="lg:col-span-5 flex flex-col gap-4">
          <SectionCard
            moduleNumber="Upload & Ingestion Gate"
            title="Specimen Upload & Preview"
            subtitle="Accepts standard JPG, JPEG, and PNG agricultural leaf imagery"
          >
            <div className="flex flex-col gap-4">
              {/* Dropzone */}
              <div
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`relative border-2 border-dashed rounded-xl p-6 flex flex-col items-center justify-center gap-3 transition-colors cursor-pointer select-none ${
                  previewUrl
                    ? 'border-[#175D44] bg-[#E5F8ED]/30'
                    : 'border-[#BFC9C2] hover:border-[#175D44] bg-[#F7F6EF]'
                }`}
              >
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  accept=".jpg,.jpeg,.png"
                  className="hidden"
                />

                {previewUrl ? (
                  <div className="relative w-full aspect-square max-h-72 rounded-lg overflow-hidden border border-[#E2E7DF] shadow-inner bg-black/5 flex items-center justify-center">
                    <img
                      src={previewUrl}
                      alt="Uploaded leaf specimen"
                      className="w-full h-full object-contain"
                    />
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center py-8 text-center text-[#404943] gap-2">
                    <div className="w-12 h-12 rounded-xl bg-[#E0F2E8] text-[#175D44] flex items-center justify-center mb-1">
                      <span className="material-symbols-outlined text-[28px]">add_photo_alternate</span>
                    </div>
                    <span className="font-semibold text-sm text-[#0F1F18]">
                      Click to browse or drop specimen image
                    </span>
                    <span className="text-xs text-[#707973]">
                      Supports JPG, JPEG, PNG (up to 10 MB)
                    </span>
                  </div>
                )}
              </div>

              {/* File Meta Pill */}
              {selectedFile && (
                <div className="p-3 bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] flex items-center justify-between text-xs font-mono">
                  <div className="flex items-center gap-2 truncate pr-2">
                    <span className="material-symbols-outlined text-[#175D44] text-[18px]">
                      description
                    </span>
                    <span className="truncate text-[#0F1F18] font-medium">{selectedFile.name}</span>
                  </div>
                  <span className="text-[#707973] shrink-0">
                    {(selectedFile.size / 1024).toFixed(1)} KB
                  </span>
                </div>
              )}

              {/* Error Alert */}
              {error && (
                <div className="p-3.5 rounded-xl bg-[#FFDAD6] border border-[#FFDAD6] text-[#93000A] text-xs flex items-center gap-2.5">
                  <span className="material-symbols-outlined text-[18px]">error</span>
                  <span className="leading-snug">{error}</span>
                </div>
              )}

              {/* Actions */}
              <div className="flex items-center gap-3 pt-1">
                <button
                  onClick={handleAnalyze}
                  disabled={!selectedFile || loading}
                  className={`flex-1 py-2.5 px-4 rounded-xl font-semibold text-xs flex items-center justify-center gap-2 transition-all shadow-xs ${
                    !selectedFile || loading
                      ? 'bg-[#BFC9C2] text-white cursor-not-allowed'
                      : 'bg-[#175D44] text-white hover:bg-[#34765B]'
                  }`}
                >
                  {loading ? (
                    <>
                      <span className="material-symbols-outlined text-[18px] animate-spin">
                        progress_activity
                      </span>
                      <span>Extracting 32D Features...</span>
                    </>
                  ) : (
                    <>
                      <span className="material-symbols-outlined text-[18px]">biotech</span>
                      <span>Analyze Specimen</span>
                    </>
                  )}
                </button>

                {selectedFile && (
                  <button
                    onClick={handleReset}
                    disabled={loading}
                    className="py-2.5 px-3 rounded-xl border border-[#BFC9C2] text-[#404943] hover:text-[#0F1F18] hover:bg-[#F7F6EF] text-xs font-semibold transition-colors"
                  >
                    Clear
                  </button>
                )}
              </div>
            </div>
          </SectionCard>
        </div>

        {/* Right Column: Preprocessing & Latent Insights (7 cols) */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          {analysisResult ? (
            <>
              {/* Preprocessing Diagnostics & Quality Validation Card */}
              <SectionCard
                moduleNumber="Stage 01 • Diagnostics"
                title="Validation & Preprocessing Integrity"
                subtitle="Verification against geometry, EXIF orientation, color mode standardization, and blur variance"
                badge="Ingestion Verified"
              >
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1">
                  <div className="p-3 bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] flex flex-col">
                    <span className="font-mono text-[10px] text-[#707973] uppercase">Format & Geometry</span>
                    <strong className="text-sm text-[#0F1F18] mt-0.5">
                      {analysisResult.validation.format} ({analysisResult.validation.raw_width}×{analysisResult.validation.raw_height})
                    </strong>
                    <span className="text-[10px] text-[#175D44] mt-1 font-mono">
                      {analysisResult.validation.exif_orientation_corrected ? 'EXIF Transposed' : 'Natural Orientation'}
                    </span>
                  </div>

                  <div className="p-3 bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] flex flex-col">
                    <span className="font-mono text-[10px] text-[#707973] uppercase">Mode & Canvas</span>
                    <strong className="text-sm text-[#0F1F18] mt-0.5">
                      {analysisResult.validation.original_color_mode || 'RGB'} → RGB
                    </strong>
                    <span className="text-[10px] text-[#175D44] mt-1 font-mono">256 × 256 Lanczos</span>
                  </div>

                  <div className="p-3 bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] flex flex-col">
                    <span className="font-mono text-[10px] text-[#707973] uppercase">Laplacian Sharpness</span>
                    <strong className="text-sm text-[#0F1F18] mt-0.5">
                      {analysisResult.validation.blur_score}
                    </strong>
                    <span
                      className={`text-[10px] font-mono mt-1 ${
                        analysisResult.validation.is_blurry ? 'text-[#6C4C00]' : 'text-[#175D44]'
                      }`}
                    >
                      {analysisResult.validation.is_blurry ? 'Natural Focus Variance' : 'High Edge Definition'}
                    </span>
                  </div>

                  <div className="p-3 bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] flex flex-col">
                    <span className="font-mono text-[10px] text-[#707973] uppercase">Dominant Tone</span>
                    <strong className="text-xs text-[#0F1F18] mt-1 truncate">
                      {analysisResult.dominant_color_tone.replace(/_/g, ' ')}
                    </strong>
                    <span className="text-[10px] text-[#175D44] mt-1 font-mono">HSV Partition</span>
                  </div>
                </div>
              </SectionCard>

              {/* Unsupervised Cluster Assignment & PCA Coordinates */}
              <SectionCard
                moduleNumber="Stage 02 • Latent Space"
                title="Unsupervised Visual Cluster Assignments"
                subtitle="Mapped into calibrated K-Means and PCA feature representations (Seed 42)"
              >
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
                  {/* K=2 Card */}
                  <div className="p-4 rounded-xl bg-[#E0F2E8]/60 border border-[#BFC9C2]/40 flex flex-col gap-2">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-[10px] text-[#175D44] font-bold uppercase">
                        Primary Metric Solution
                      </span>
                      <span className="px-2 py-0.5 rounded font-mono text-[10px] bg-[#175D44] text-white font-bold">
                        K = 2
                      </span>
                    </div>
                    <div className="font-headline font-bold text-lg text-[#0F1F18]">
                      Cluster {analysisResult.clustering.k2.cluster_id} Assigned
                    </div>
                    <p className="text-xs text-[#404943] leading-relaxed">
                      {analysisResult.clustering.k2.characteristics}
                    </p>
                  </div>

                  {/* K=4 Card */}
                  <div className="p-4 rounded-xl bg-[#F7F6EF] border border-[#E2E7DF] flex flex-col gap-2">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-[10px] text-[#404943] uppercase font-bold">
                        Exploratory Sub-partition
                      </span>
                      <span className="px-2 py-0.5 rounded font-mono text-[10px] bg-[#404943] text-white font-bold">
                        K = 4
                      </span>
                    </div>
                    <div className="font-headline font-bold text-lg text-[#0F1F18]">
                      Cluster {analysisResult.clustering.k4.cluster_id} Assigned
                    </div>
                    <p className="text-xs text-[#404943] leading-relaxed">
                      {analysisResult.clustering.k4.characteristics}
                    </p>
                  </div>
                </div>

                {/* PCA Latent 2D Projection Banner */}
                <div className="mt-4 p-3 bg-white rounded-xl border border-[#E2E7DF] flex items-center justify-between text-xs font-mono">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-[#175D44] text-[18px]">
                      scatter_plot
                    </span>
                    <span className="text-[#0F1F18] font-semibold">PCA 2D Coordinates:</span>
                    <span className="text-[#175D44]">
                      PC1 (38.6%) = <strong>{analysisResult.pca_projection.x.toFixed(3)}</strong>
                    </span>
                    <span className="text-[#404943]">|</span>
                    <span className="text-[#175D44]">
                      PC2 (13.6%) = <strong>{analysisResult.pca_projection.y.toFixed(3)}</strong>
                    </span>
                  </div>
                  <span className="text-[10px] text-[#707973] hidden sm:inline">
                    52.1% Total Visual Variance
                  </span>
                </div>
              </SectionCard>
            </>
          ) : (
            <div className="h-full min-h-[320px] bg-[#F7F6EF] rounded-2xl border border-dashed border-[#BFC9C2] flex flex-col items-center justify-center p-8 text-center text-[#707973]">
              <span className="material-symbols-outlined text-4xl mb-2 text-[#BFC9C2]">
                analytics
              </span>
              <h3 className="font-headline font-semibold text-sm text-[#0F1F18]">
                Awaiting Specimen Upload
              </h3>
              <p className="text-xs text-[#707973] max-w-sm mt-1 leading-relaxed">
                Select or drop an agricultural foliar specimen to run 32D classical feature extraction, compute sharpness diagnostics, and retrieve nearest canonical specimens.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Analysis Output Section: Nearest Specimens & Feature Tensor */}
      {analysisResult && (
        <div className="flex flex-col gap-6">
          {/* Nearest Reference Specimens in Standardized 32D Descriptor Space */}
          <SectionCard
            moduleNumber="Stage 03 • Proximity Retrieval"
            title="Nearest Reference Specimens in Frozen Repository"
            subtitle="Ranked by Euclidean distance across 32 standardized descriptors (z = (x - μ)/σ). Proximity index 1/(1+d) is an uncalibrated geometric score, NOT a biological diagnosis."
            badge="2,596 Reference Images"
          >
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 pt-1">
              {analysisResult.nearest_specimens.map((specimen: NearestSpecimen) => (
                <div
                  key={specimen.image_id}
                  className="bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] overflow-hidden flex flex-col justify-between hover:border-[#175D44] transition-all shadow-2xs group"
                >
                  {/* Thumbnail */}
                  <div className="relative aspect-square w-full bg-black/5 overflow-hidden flex items-center justify-center">
                    <img
                      src={specimen.image_url}
                      alt={specimen.image_id}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      onError={(e) => {
                        ;(e.target as HTMLElement).style.display = 'none'
                      }}
                    />
                    <div className="absolute top-2 left-2 px-1.5 py-0.5 rounded font-mono text-[9px] bg-black/60 text-white backdrop-blur-xs">
                      #{specimen.rank}
                    </div>
                    <div
                      className={`absolute top-2 right-2 px-1.5 py-0.5 rounded font-mono text-[9px] font-bold ${
                        specimen.condition_status.toLowerCase() === 'healthy'
                          ? 'bg-[#C3EFAA] text-[#2B4F1C]'
                          : 'bg-[#FFDAD6] text-[#93000A]'
                      }`}
                    >
                      {specimen.condition_status}
                    </div>
                  </div>

                  {/* Specimen Info */}
                  <div className="p-3 flex flex-col gap-1.5 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="font-mono font-bold text-[#175D44] text-[11px]">
                        {specimen.image_id}
                      </span>
                      <span className="font-mono text-[10px] text-[#707973] uppercase">
                        {specimen.dataset_source}
                      </span>
                    </div>

                    <div className="font-semibold text-[#0F1F18] truncate">
                      {specimen.crop_name}
                    </div>

                    <div className="text-[11px] text-[#404943] truncate">
                      {specimen.disease_name}
                    </div>

                    <div className="pt-2 border-t border-[#E2E7DF] flex flex-col gap-1 font-mono text-[10px]">
                      <div className="flex justify-between items-center">
                        <span className="text-[#707973]">32D Distance (d):</span>
                        <strong className="text-[#0F1F18] bg-white px-1.5 py-0.5 rounded border border-[#E2E7DF]">
                          {specimen.euclidean_distance.toFixed(4)}
                        </strong>
                      </div>
                      <div className="flex justify-between items-center text-[9px]">
                        <span className="text-[#707973]">Proximity 1/(1+d):</span>
                        <strong className="text-[#175D44]">
                          {(specimen.visual_similarity_score * 100).toFixed(1)}%
                        </strong>
                      </div>
                    </div>

                    {/* Action Button */}
                    <button
                      onClick={() => {
                        if (onNavigateToSpecimen) {
                          onNavigateToSpecimen(specimen.image_id)
                        } else {
                          setModalSpecimenId(specimen.image_id)
                        }
                      }}
                      className="mt-2 w-full py-1.5 px-2 rounded-lg bg-white border border-[#BFC9C2]/50 hover:bg-[#E0F2E8] hover:text-[#175D44] text-[11px] font-semibold text-[#0F1F18] transition-colors flex items-center justify-center gap-1"
                    >
                      <span className="material-symbols-outlined text-[14px]">visibility</span>
                      <span>Inspect Details</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </SectionCard>

          {/* 32-Dimensional Continuous Visual Feature Tensor Card */}
          <SectionCard
            moduleNumber="Stage 04 • Feature Vectors"
            title="Extracted 32-Dimensional Visual Feature Representation"
            subtitle={
              featureScaleMode === 'standardized'
                ? 'Standardized z-scores: z = (x - μ) / σ computed using frozen StandardScaler (zero mean, unit variance) passed directly to K-Means and Euclidean distance.'
                : 'Raw extracted continuous descriptors in natural units (RGB [0,255], Hue [0,360°], GLCM [0,1], Contour [px]).'
            }
            badge="32 Features"
            actions={
              <div className="flex flex-wrap items-center gap-2">
                {/* Scale Mode Toggle */}
                <div className="flex items-center gap-1 bg-[#E0F2E8]/60 p-1 rounded-lg border border-[#BFC9C2]/40 text-xs font-mono">
                  <button
                    onClick={() => setFeatureScaleMode('standardized')}
                    className={`px-2.5 py-1 rounded-md font-semibold text-[11px] transition-all ${
                      featureScaleMode === 'standardized'
                        ? 'bg-[#175D44] text-white shadow-xs'
                        : 'text-[#404943] hover:text-[#0F1F18]'
                    }`}
                  >
                    Standardized (Z-Scores)
                  </button>
                  <button
                    onClick={() => setFeatureScaleMode('raw')}
                    className={`px-2.5 py-1 rounded-md font-semibold text-[11px] transition-all ${
                      featureScaleMode === 'raw'
                        ? 'bg-[#175D44] text-white shadow-xs'
                        : 'text-[#404943] hover:text-[#0F1F18]'
                    }`}
                  >
                    Raw Natural Units
                  </button>
                </div>

                {/* Feature Family Tabs */}
                <div className="flex items-center gap-1 bg-[#F7F6EF] p-1 rounded-lg border border-[#E2E7DF] text-xs font-mono">
                  <button
                    onClick={() => setActiveFeatureTab('color')}
                    className={`px-3 py-1 rounded-md font-semibold transition-all ${
                      activeFeatureTab === 'color'
                        ? 'bg-[#175D44] text-white shadow-xs'
                        : 'text-[#404943] hover:text-[#0F1F18]'
                    }`}
                  >
                    Color ({analysisResult.feature_counts.color_moments})
                  </button>
                  <button
                    onClick={() => setActiveFeatureTab('texture')}
                    className={`px-3 py-1 rounded-md font-semibold transition-all ${
                      activeFeatureTab === 'texture'
                        ? 'bg-[#175D44] text-white shadow-xs'
                        : 'text-[#404943] hover:text-[#0F1F18]'
                    }`}
                  >
                    GLCM Texture ({analysisResult.feature_counts.glcm_texture})
                  </button>
                  <button
                    onClick={() => setActiveFeatureTab('shape')}
                    className={`px-3 py-1 rounded-md font-semibold transition-all ${
                      activeFeatureTab === 'shape'
                        ? 'bg-[#175D44] text-white shadow-xs'
                        : 'text-[#404943] hover:text-[#0F1F18]'
                    }`}
                  >
                    Contour Shape ({analysisResult.feature_counts.contour_morphology})
                  </button>
                </div>
              </div>
            }
          >
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-3 pt-1">
              {Object.entries(
                (featureScaleMode === 'standardized'
                  ? analysisResult.features_grouped_standardized?.[activeFeatureTab] ||
                    analysisResult.features_grouped[activeFeatureTab]
                  : analysisResult.features_grouped_raw?.[activeFeatureTab] ||
                    analysisResult.features_grouped[activeFeatureTab]) || {}
              ).map(([featName, val]: [string, number]) => {
                const meta = analysisResult.feature_definitions?.[featName]
                return (
                  <div
                    key={featName}
                    className="p-3 bg-[#F7F6EF] rounded-xl border border-[#E2E7DF] flex flex-col justify-between"
                  >
                    <div className="flex items-center justify-between gap-1">
                      <span className="font-mono text-[11px] text-[#404943] truncate font-semibold" title={featName}>
                        {featName}
                      </span>
                      <span className="font-mono text-[9px] px-1.5 py-0.2 rounded bg-white border border-[#E2E7DF] text-[#707973] shrink-0">
                        {featureScaleMode === 'standardized' ? 'z-score' : meta?.range || 'float64'}
                      </span>
                    </div>

                    <div className="flex items-baseline justify-between mt-2">
                      <span className={`font-headline font-bold text-base ${featureScaleMode === 'standardized' ? (val >= 0 ? 'text-[#175D44]' : 'text-[#93000A]') : 'text-[#0F1F18]'}`}>
                        {featureScaleMode === 'standardized' && val > 0 ? `+${val.toFixed(4)}` : val.toFixed(4)}
                      </span>
                      <span className="font-mono text-[10px] text-[#707973]">
                        {featureScaleMode === 'standardized' ? 'σ deviation' : 'measured'}
                      </span>
                    </div>

                    {meta?.description && (
                      <p className="text-[10px] text-[#707973] mt-1.5 leading-snug line-clamp-2 border-t border-[#E2E7DF]/60 pt-1">
                        {meta.description}
                      </p>
                    )}
                  </div>
                )
              })}
            </div>
          </SectionCard>
        </div>
      )}

      {/* Modal Specimen Inspector if requested */}
      {modalSpecimenId && (
        <SpecimenModal
          imageId={modalSpecimenId}
          onClose={() => setModalSpecimenId(null)}
        />
      )}
    </div>
  )
}
