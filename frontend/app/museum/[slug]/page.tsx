'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import ZoneCard from '@/components/ZoneCard'
import HealthBanner from '@/components/HealthBanner'
import TrendChart from '@/components/TrendChart'
import type { MuseumDashboard } from '@/lib/api'

export default function MuseumPage() {
  const params = useParams()
  const slug = params.slug as string
  const [data, setData] = useState<MuseumDashboard | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [retryCount, setRetryCount] = useState(0)
  const [view, setView] = useState<'overview' | 'trends'>('overview')

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://conservatwin-platform.onrender.com'

    async function fetchData(attempt: number) {
      try {
        const r = await fetch(`${apiUrl}/api/public/${slug}`, { signal: AbortSignal.timeout(45000) })
        if (!r.ok) throw new Error('Museum not found')
        const json = await r.json()
        setData(json)
        setLoading(false)
      } catch (e: any) {
        if (attempt < 3) {
          setRetryCount(attempt + 1)
          setTimeout(() => fetchData(attempt + 1), 3000)
        } else {
          setError(e.message || 'Failed to connect to server')
          setLoading(false)
        }
      }
    }

    fetchData(0)
  }, [slug])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-2 h-2 rounded-full bg-brass animate-pulse-glow" />
            <span className="text-neutral-500 font-mono text-sm">Loading heritage data...</span>
          </div>
          {retryCount > 0 && (
            <p className="text-xs text-neutral-600 font-mono">
              Server is waking up... attempt {retryCount}/3 (free tier cold start ~30s)
            </p>
          )}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-display text-neutral-400 mb-2">Museum Not Found</h1>
          <p className="text-neutral-600 mb-4">{error}</p>
          <Link href="/" className="text-brass hover:underline text-sm">Back to Home</Link>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex items-center gap-3">
          <div className="w-2 h-2 rounded-full bg-brass animate-pulse-glow" />
          <span className="text-neutral-500 font-mono text-sm">Loading heritage data...</span>
        </div>
      </div>
    )
  }

  const { museum, zones, overall_health } = data

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b border-neutral-800 bg-surface-1">
        <div className="max-w-6xl mx-auto px-6 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/" className="flex items-center gap-2 text-neutral-500 hover:text-brass transition-colors">
                <div className="w-6 h-6 rounded-full bg-brass/20 flex items-center justify-center">
                  <div className="w-2 h-2 rounded-full bg-brass" />
                </div>
                <span className="font-display text-sm">ConservaTwin</span>
              </Link>
              <span className="text-neutral-700">/</span>
              <span className="text-neutral-300 font-medium">{museum.name}</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${
                  overall_health.status === 'excellent' || overall_health.status === 'good' ? 'bg-status-stable'
                  : overall_health.status === 'critical' ? 'bg-status-critical animate-pulse-glow'
                  : 'bg-status-elevated'
                }`} />
                <span className="text-xs font-mono text-neutral-500">LIVE</span>
              </div>
              <span className="text-xs text-neutral-600">{museum.location}</span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Health Banner */}
        <HealthBanner health={overall_health} zoneCount={zones.length} />

        {/* View Toggle */}
        <div className="flex gap-1 mb-8 bg-surface-2 rounded-lg p-1 w-fit">
          <button
            onClick={() => setView('overview')}
            className={`px-4 py-1.5 rounded text-sm transition-colors ${
              view === 'overview' ? 'bg-surface-3 text-brass' : 'text-neutral-500 hover:text-neutral-300'
            }`}
          >
            Zone Overview
          </button>
          <button
            onClick={() => setView('trends')}
            className={`px-4 py-1.5 rounded text-sm transition-colors ${
              view === 'trends' ? 'bg-surface-3 text-brass' : 'text-neutral-500 hover:text-neutral-300'
            }`}
          >
            Trend Analysis
          </button>
        </div>

        {view === 'overview' ? (
          <div className="grid md:grid-cols-2 gap-6">
            {zones.map((z, i) => (
              <div key={i} className="animate-fade-in" style={{ animationDelay: `${i * 0.1}s` }}>
                <ZoneCard data={z} />
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-6">
            {zones.map((z, i) => (
              <div key={i} className="animate-fade-in" style={{ animationDelay: `${i * 0.1}s` }}>
                <div className="text-sm font-medium mb-2 text-neutral-300">{z.zone.name}</div>
                <TrendChart
                  readings={z.readings_24h}
                  tempRange={z.zone.targets.temp}
                  rhRange={z.zone.targets.rh}
                />
              </div>
            ))}
          </div>
        )}

        {/* Museum Info Footer */}
        <div className="mt-12 pt-8 border-t border-neutral-800">
          <div className="flex items-center justify-between text-xs text-neutral-600">
            <div>
              Monitoring since {new Date(museum.created_at).toLocaleDateString()}
            </div>
            <div className="flex items-center gap-2">
              <span>Powered by</span>
              <Link href="/" className="text-brass/50 hover:text-brass">ConservaTwin</Link>
              <span>— open-source heritage preservation</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
