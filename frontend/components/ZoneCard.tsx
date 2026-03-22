'use client'

import PRIGauge from './PRIGauge'
import type { ZoneData } from '@/lib/api'

const materialLabels: Record<string, string> = {
  general: 'General',
  oil_painting: 'Oil Painting',
  watercolor: 'Watercolor',
  textile: 'Textile',
  wood: 'Wood',
  metal: 'Metal',
  paper: 'Paper/Manuscript',
  ceramic: 'Ceramic',
  photograph: 'Photograph',
  stone: 'Stone/Marble',
}

const riskBorder: Record<string, string> = {
  stable: 'border-status-stable/20',
  elevated: 'border-status-elevated/20',
  high: 'border-status-high/20',
  critical: 'border-status-critical/30',
}

export default function ZoneCard({ data }: { data: ZoneData }) {
  const { zone, current, pri, recommendations, recent_alerts } = data
  const borderClass = riskBorder[pri.risk_level] || 'border-neutral-800'

  return (
    <div className={`bg-surface-2 border ${borderClass} rounded-lg p-6 transition-all hover:border-brass/20`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-base font-medium">{zone.name}</h3>
          <p className="text-xs text-neutral-500 mt-1">{zone.description}</p>
          <span className="inline-block mt-2 text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded bg-surface-3 text-brass/70">
            {materialLabels[zone.material_type] || zone.material_type}
          </span>
        </div>
        <PRIGauge value={pri.value} size={100} />
      </div>

      {/* Current readings */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="bg-surface-3 rounded px-3 py-2">
          <div className="text-[10px] text-neutral-500 font-mono uppercase">Temperature</div>
          <div className="flex items-baseline gap-1 mt-1">
            <span className={`text-xl font-mono font-medium ${
              current.temperature < zone.targets.temp[0] || current.temperature > zone.targets.temp[1]
                ? 'text-status-high' : 'text-status-stable'
            }`}>
              {current.temperature?.toFixed(1) ?? '--'}
            </span>
            <span className="text-xs text-neutral-500">°C</span>
          </div>
          <div className="text-[10px] text-neutral-600 mt-0.5">
            Target: {zone.targets.temp[0]}–{zone.targets.temp[1]}°C
          </div>
        </div>
        <div className="bg-surface-3 rounded px-3 py-2">
          <div className="text-[10px] text-neutral-500 font-mono uppercase">Humidity</div>
          <div className="flex items-baseline gap-1 mt-1">
            <span className={`text-xl font-mono font-medium ${
              current.humidity < zone.targets.rh[0] || current.humidity > zone.targets.rh[1]
                ? 'text-status-high' : 'text-status-stable'
            }`}>
              {current.humidity?.toFixed(1) ?? '--'}
            </span>
            <span className="text-xs text-neutral-500">%RH</span>
          </div>
          <div className="text-[10px] text-neutral-600 mt-0.5">
            Target: {zone.targets.rh[0]}–{zone.targets.rh[1]}%
          </div>
        </div>
      </div>

      {/* Risk factors */}
      {pri.factors.length > 0 && (
        <div className="mb-4">
          <div className="text-[10px] font-mono uppercase text-neutral-500 mb-1">Risk Factors</div>
          {pri.factors.map((f, i) => (
            <div key={i} className="text-xs text-status-high flex items-start gap-1.5 mt-1">
              <span className="mt-0.5">&#9888;</span>
              <span>{f}</span>
            </div>
          ))}
        </div>
      )}

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <div className="mb-4">
          <div className="text-[10px] font-mono uppercase text-neutral-500 mb-1">AI Recommendations</div>
          {recommendations.slice(0, 3).map((r, i) => (
            <div key={i} className={`text-xs mt-1.5 pl-3 border-l-2 ${
              r.priority === 'immediate' ? 'border-status-critical text-neutral-300'
              : r.priority === 'soon' ? 'border-status-elevated text-neutral-400'
              : 'border-neutral-700 text-neutral-500'
            }`}>
              <span className="font-mono text-[10px] uppercase mr-1">[{r.priority}]</span>
              {r.action}
            </div>
          ))}
        </div>
      )}

      {/* Recent alerts */}
      {recent_alerts.length > 0 && (
        <div>
          <div className="text-[10px] font-mono uppercase text-neutral-500 mb-1">Recent Alerts</div>
          {recent_alerts.slice(0, 3).map((a, i) => (
            <div key={i} className="text-xs text-neutral-500 mt-1 flex items-start gap-2">
              <span className={`inline-block w-1.5 h-1.5 rounded-full mt-1 flex-shrink-0 ${
                a.severity === 'critical' ? 'bg-status-critical' : 'bg-status-elevated'
              }`} />
              <span>{a.message.slice(0, 100)}</span>
            </div>
          ))}
        </div>
      )}

      {/* Last updated */}
      {current.timestamp && (
        <div className="text-[10px] text-neutral-600 mt-4 font-mono">
          Last reading: {new Date(current.timestamp).toLocaleString()}
        </div>
      )}
    </div>
  )
}
