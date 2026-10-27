import React from 'react'
import { AppIcon } from './AppIcon'

interface KPICardProps {
  label: string
  value: string | number
  unit?: string
  icon: string
  iconColor?: string
  progressLabel?: string
  progressPercent?: number
  secondaryLabel?: string
  footerNote?: string
}

export const KPICard: React.FC<KPICardProps> = ({
  label,
  value,
  unit,
  icon,
  iconColor = 'text-[#175D44]',
  progressLabel,
  progressPercent,
  secondaryLabel,
  footerNote,
}) => {
  return (
    <div className="bg-[#FFFFFF] rounded-xl p-4 flex flex-col justify-between border border-[#E2E7DF] shadow-[0_1px_3px_rgba(0,0,0,0.03)] hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex flex-col">
          <span className="font-mono text-[10px] text-[#404943] uppercase tracking-wider font-medium">
            {label}
          </span>
          <div className="flex items-baseline gap-1.5 mt-1">
            <span className="font-headline text-2xl sm:text-3xl font-semibold tracking-tight text-[#0F1F18]">
              {typeof value === 'number' ? value.toLocaleString() : value}
            </span>
            {unit && (
              <span className="font-mono text-xs text-[#404943] font-normal">{unit}</span>
            )}
          </div>
        </div>
        <div className="w-9 h-9 rounded-lg bg-[#E0F2E8] flex items-center justify-center shrink-0">
          <AppIcon name={icon} className={`w-5 h-5 ${iconColor}`} />
        </div>
      </div>

      <div className="mt-4 flex flex-col gap-1.5">
        {(progressLabel || secondaryLabel) && (
          <div className="flex justify-between items-center text-[11px] text-[#404943]">
            <span>{progressLabel}</span>
            {secondaryLabel && (
              <span className="font-mono font-medium text-[#0F1F18]">{secondaryLabel}</span>
            )}
          </div>
        )}

        {progressPercent !== undefined && (
          <div className="w-full h-1.5 rounded-full bg-[#E0F2E8] overflow-hidden flex">
            <div
              className="bg-[#175D44] h-full transition-all duration-500"
              style={{ width: `${Math.min(100, Math.max(0, progressPercent))}%` }}
            />
          </div>
        )}

        {footerNote && (
          <div className="flex items-center gap-1 text-[11px] text-[#404943]/80 font-mono">
            {footerNote}
          </div>
        )}
      </div>
    </div>
  )
}
