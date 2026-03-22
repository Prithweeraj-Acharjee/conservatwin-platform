'use client'

interface HealthData {
  average_pri: number
  worst_pri: number
  status: string
  zones_at_risk: number
}

const statusConfig: Record<string, { color: string; bg: string; label: string }> = {
  excellent: { color: 'text-status-stable', bg: 'bg-status-stable/10', label: 'Excellent' },
  good: { color: 'text-status-stable', bg: 'bg-status-stable/10', label: 'Good' },
  'needs attention': { color: 'text-status-elevated', bg: 'bg-status-elevated/10', label: 'Needs Attention' },
  critical: { color: 'text-status-critical', bg: 'bg-status-critical/10', label: 'Critical' },
  'no data': { color: 'text-neutral-500', bg: 'bg-neutral-800', label: 'No Data' },
}

export default function HealthBanner({ health, zoneCount }: { health: HealthData; zoneCount: number }) {
  const config = statusConfig[health.status] || statusConfig['no data']

  return (
    <div className={`${config.bg} border border-neutral-800 rounded-lg p-6 mb-8`}>
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-4">
          <div className={`w-3 h-3 rounded-full ${
            health.status === 'excellent' || health.status === 'good' ? 'bg-status-stable'
            : health.status === 'needs attention' ? 'bg-status-elevated animate-pulse-glow'
            : health.status === 'critical' ? 'bg-status-critical animate-pulse-glow'
            : 'bg-neutral-600'
          }`} />
          <div>
            <div className={`text-lg font-medium ${config.color}`}>
              Overall Status: {config.label}
            </div>
            <div className="text-sm text-neutral-500 mt-0.5">
              {zoneCount} monitored zones
            </div>
          </div>
        </div>

        <div className="flex gap-8">
          <div className="text-center">
            <div className="text-2xl font-mono font-medium text-neutral-300">{health.average_pri}</div>
            <div className="text-[10px] font-mono uppercase text-neutral-500 mt-0.5">Avg PRI</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-mono font-medium ${
              health.worst_pri >= 70 ? 'text-status-critical'
              : health.worst_pri >= 45 ? 'text-status-high'
              : 'text-neutral-300'
            }`}>{health.worst_pri}</div>
            <div className="text-[10px] font-mono uppercase text-neutral-500 mt-0.5">Worst PRI</div>
          </div>
          {health.zones_at_risk > 0 && (
            <div className="text-center">
              <div className="text-2xl font-mono font-medium text-status-critical">{health.zones_at_risk}</div>
              <div className="text-[10px] font-mono uppercase text-neutral-500 mt-0.5">Zones at Risk</div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
