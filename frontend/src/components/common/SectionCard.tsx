import React from 'react'

interface SectionCardProps {
  moduleNumber?: string
  title: string
  subtitle?: string
  badge?: string
  actions?: React.ReactNode
  children: React.ReactNode
  className?: string
}

export const SectionCard: React.FC<SectionCardProps> = ({
  moduleNumber,
  title,
  subtitle,
  badge,
  actions,
  children,
  className = '',
}) => {
  return (
    <div
      className={`bg-[#FFFFFF] rounded-xl p-5 border border-[#E2E7DF] shadow-[0_1px_3px_rgba(0,0,0,0.03)] flex flex-col gap-4 ${className}`}
    >
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-[#E2E7DF]/60">
        <div className="flex flex-col">
          {moduleNumber && (
            <span className="font-mono text-[10px] uppercase tracking-wider text-[#175D44] font-semibold">
              {moduleNumber}
            </span>
          )}
          <h2 className="font-headline text-lg sm:text-xl font-semibold text-[#0F1F18] leading-snug">
            {title}
          </h2>
          {subtitle && (
            <p className="text-xs text-[#404943] leading-relaxed mt-0.5">{subtitle}</p>
          )}
        </div>
        <div className="flex items-center gap-2 self-start sm:self-auto">
          {badge && (
            <span className="px-2.5 py-1 rounded bg-[#E0F2E8] text-[#175D44] font-mono text-[11px] font-medium border border-[#BFC9C2]/30">
              {badge}
            </span>
          )}
          {actions}
        </div>
      </div>
      <div>{children}</div>
    </div>
  )
}
