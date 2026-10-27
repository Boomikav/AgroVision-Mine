import React from 'react'
import {
  GitBranch,
  ImagePlus,
  LineChart,
  ArrowRight,
  Maximize2,
  Sparkles,
  Microscope,
  Focus,
  Zap,
  CircleDot,
  Bug,
  Crosshair,
  Check,
  CheckCircle2,
  ChevronRight,
  X,
  Minimize2,
  Copy,
  LayoutDashboard,
  Database,
  Layers,
  FileText,
  Download,
  Leaf,
  AlertCircle,
  FileDown,
  FolderArchive,
  ScatterChart,
  Grid,
  GitFork,
  Info,
  Tag,
  Menu,
  BookOpen,
  Images,
  PieChart,
  Play,
  Sprout,
  Loader2,
  BarChart2,
  RotateCcw,
  CheckSquare,
  Search,
  SearchX,
  ArrowLeftRight,
  Table,
  Clock,
  Compass,
  BadgeCheck,
  ShieldCheck,
  Box,
  Eye,
  AlertTriangle,
  HelpCircle,
  type LucideIcon
} from 'lucide-react'

const ICON_MAP: Record<string, LucideIcon> = {
  account_tree: GitBranch,
  add_photo_alternate: ImagePlus,
  analytics: LineChart,
  arrow_forward: ArrowRight,
  aspect_ratio: Maximize2,
  auto_awesome_motion: Sparkles,
  biotech: Microscope,
  blur_on: Focus,
  bolt: Zap,
  bubble_chart: CircleDot,
  bug_report: Bug,
  center_focus_strong: Crosshair,
  check: Check,
  check_circle: CheckCircle2,
  chevron_right: ChevronRight,
  close: X,
  compress: Minimize2,
  content_copy: Copy,
  coronavirus: Bug,
  dashboard: LayoutDashboard,
  database: Database,
  dataset: Layers,
  description: FileText,
  download: Download,
  eco: Leaf,
  error: AlertCircle,
  file_download: FileDown,
  folder_zip: FolderArchive,
  grain: ScatterChart,
  grid_view: Grid,
  hub: GitFork,
  info: Info,
  label: Tag,
  menu: Menu,
  menu_book: BookOpen,
  photo_library: Images,
  pie_chart: PieChart,
  play_arrow: Play,
  potted_plant: Sprout,
  progress_activity: Loader2,
  query_stats: BarChart2,
  restart_alt: RotateCcw,
  rule: CheckSquare,
  scatter_plot: ScatterChart,
  search: Search,
  search_off: SearchX,
  sync_alt: ArrowLeftRight,
  table_rows: Table,
  timer: Clock,
  travel_explore: Compass,
  verified: BadgeCheck,
  verified_user: ShieldCheck,
  view_in_ar: Box,
  visibility: Eye,
  warning: AlertTriangle,
  warning_amber: AlertTriangle,
}

interface AppIconProps {
  name: string
  className?: string
  size?: number | string
}

export const AppIcon: React.FC<AppIconProps> = ({ name, className = '', size }) => {
  const normalizedKey = name.trim().toLowerCase()
  const IconComponent = ICON_MAP[normalizedKey] || HelpCircle

  // If progress_activity is used, guarantee spinning
  const isSpinner = normalizedKey === 'progress_activity'
  const combinedClass = isSpinner && !className.includes('animate-spin')
    ? `${className} animate-spin`
    : className

  let resolvedSize: number | string | undefined = size
  if (resolvedSize === undefined) {
    const pxMatch = className.match(/text-\[(\d+)px\]/)
    if (pxMatch) {
      resolvedSize = parseInt(pxMatch[1], 10)
    } else if (className.includes('text-4xl')) {
      resolvedSize = 36
    } else if (className.includes('text-3xl')) {
      resolvedSize = 30
    } else if (className.includes('text-2xl')) {
      resolvedSize = 24
    } else if (className.includes('text-xl')) {
      resolvedSize = 20
    } else if (className.includes('text-lg')) {
      resolvedSize = 18
    } else if (className.includes('text-sm')) {
      resolvedSize = 14
    } else if (className.includes('text-xs')) {
      resolvedSize = 12
    } else {
      resolvedSize = 18
    }
  }

  return (
    <IconComponent
      className={`inline-block shrink-0 ${combinedClass}`}
      size={resolvedSize}
      aria-hidden="true"
    />
  )
}

