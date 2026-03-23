'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

export default function LandingPage() {
  const [museums, setMuseums] = useState<any[]>([])

  useEffect(() => {
    async function load(attempt: number) {
      try {
        const r = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://conservatwin-platform.onrender.com'}/api/museums`, { signal: AbortSignal.timeout(45000) })
        const d = await r.json()
        setMuseums(d.museums || [])
      } catch {
        if (attempt < 3) setTimeout(() => load(attempt + 1), 3000)
      }
    }
    load(0)
  }, [])

  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-surface-1 to-surface-0" />
        <div className="relative max-w-5xl mx-auto px-6 pt-20 pb-24">
          <nav className="flex items-center justify-between mb-20">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-brass/20 flex items-center justify-center">
                <div className="w-3 h-3 rounded-full bg-brass" />
              </div>
              <span className="font-display text-lg tracking-wide text-brass">ConservaTwin</span>
            </div>
            <div className="flex gap-6 text-sm text-neutral-400">
              <a href="#how-it-works" className="hover:text-brass transition-colors">How it Works</a>
              <a href="#features" className="hover:text-brass transition-colors">Features</a>
              <a href="https://github.com/Prithweeraj-Acharjee/conservatwin-platform" target="_blank" className="hover:text-brass transition-colors">GitHub</a>
            </div>
          </nav>

          <div className="max-w-3xl">
            <p className="text-brass font-mono text-sm mb-4 tracking-widest uppercase">Open-Source Heritage Preservation</p>
            <h1 className="font-display text-5xl md:text-6xl font-light leading-tight mb-6">
              A medical chart for the world&apos;s art and monuments
            </h1>
            <p className="text-xl text-neutral-400 leading-relaxed mb-10 max-w-2xl">
              A $5 sensor. Free software. Any museum, temple, or historical building can monitor
              environmental conditions and receive AI-powered conservation recommendations.
            </p>
            <div className="flex gap-4">
              <a href="#live-museums" className="bg-brass text-surface-0 px-6 py-3 rounded font-medium hover:bg-brass/90 transition-colors">
                View Live Museums
              </a>
              <a href="https://github.com/Prithweeraj-Acharjee/conservatwin-platform" target="_blank" className="border border-neutral-700 px-6 py-3 rounded text-neutral-300 hover:border-brass hover:text-brass transition-colors">
                Star on GitHub
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <section className="border-y border-neutral-800 bg-surface-1">
        <div className="max-w-5xl mx-auto px-6 py-8 grid grid-cols-2 md:grid-cols-4 gap-8">
          <div>
            <div className="text-3xl font-display text-brass">$5</div>
            <div className="text-sm text-neutral-500 mt-1">Hardware cost per sensor</div>
          </div>
          <div>
            <div className="text-3xl font-display text-brass">100%</div>
            <div className="text-sm text-neutral-500 mt-1">Free & open-source</div>
          </div>
          <div>
            <div className="text-3xl font-display text-brass">10</div>
            <div className="text-sm text-neutral-500 mt-1">Material profiles</div>
          </div>
          <div>
            <div className="text-3xl font-display text-brass">24/7</div>
            <div className="text-sm text-neutral-500 mt-1">Real-time monitoring</div>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section id="how-it-works" className="max-w-5xl mx-auto px-6 py-24">
        <p className="text-brass font-mono text-sm mb-3 tracking-widest uppercase">How it Works</p>
        <h2 className="font-display text-3xl mb-16">Three steps. Ten minutes. Zero cost.</h2>

        <div className="grid md:grid-cols-3 gap-12">
          <div className="animate-fade-in">
            <div className="w-12 h-12 rounded-lg bg-surface-2 border border-neutral-800 flex items-center justify-center mb-4">
              <span className="text-brass font-mono text-lg">01</span>
            </div>
            <h3 className="text-lg font-medium mb-2">Plug in a sensor</h3>
            <p className="text-neutral-400 text-sm leading-relaxed">
              ESP32 + DHT22 — a $5 sensor the size of a matchbox. Plug it into any wall outlet.
              It reads temperature and humidity every 30 seconds.
            </p>
          </div>
          <div className="animate-fade-in" style={{ animationDelay: '0.15s' }}>
            <div className="w-12 h-12 rounded-lg bg-surface-2 border border-neutral-800 flex items-center justify-center mb-4">
              <span className="text-brass font-mono text-lg">02</span>
            </div>
            <h3 className="text-lg font-medium mb-2">Data flows to ConservaTwin</h3>
            <p className="text-neutral-400 text-sm leading-relaxed">
              Sensor data is sent to the cloud. Our Preservation Risk Index (PRI) engine calculates
              real-time stress on your artifacts based on material type.
            </p>
          </div>
          <div className="animate-fade-in" style={{ animationDelay: '0.3s' }}>
            <div className="w-12 h-12 rounded-lg bg-surface-2 border border-neutral-800 flex items-center justify-center mb-4">
              <span className="text-brass font-mono text-lg">03</span>
            </div>
            <h3 className="text-lg font-medium mb-2">Get AI recommendations</h3>
            <p className="text-neutral-400 text-sm leading-relaxed">
              Receive material-specific conservation advice. &quot;Humidity in Room 3 is too high for oil paintings.
              Activate dehumidifier or open west ventilation.&quot;
            </p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="bg-surface-1 border-y border-neutral-800">
        <div className="max-w-5xl mx-auto px-6 py-24">
          <p className="text-brass font-mono text-sm mb-3 tracking-widest uppercase">Features</p>
          <h2 className="font-display text-3xl mb-16">Industrial-grade conservation intelligence</h2>

          <div className="grid md:grid-cols-2 gap-8">
            {[
              { title: 'Preservation Risk Index', desc: 'Quantifies environmental stress from 0-100 based on deviation, stability, and rate-of-change. Different profiles for oil paintings, textiles, paper, wood, metal, ceramics, and more.' },
              { title: 'AI Conservation Advisor', desc: 'Material-aware recommendations that tell you exactly what to do. Not just "humidity is high" but "deploy dehumidifiers, oil paintings risk canvas warping at this RH level."' },
              { title: 'Anomaly Detection', desc: 'Catches sensor spikes, flatlines, drift, and impossible values. Detects HVAC degradation before it damages your collection.' },
              { title: 'Public Heritage Dashboard', desc: 'Every museum gets a live health profile page. Transparent conservation data for researchers, donors, and the public.' },
              { title: 'Multi-Tenant Platform', desc: 'Any museum registers in one API call. Add unlimited zones. Configure material types and target ranges per room.' },
              { title: '$5 Hardware', desc: 'ESP32 + DHT22 sensor. Arduino sketch included. No proprietary hardware. No vendor lock-in. Works on WiFi.' },
            ].map((f, i) => (
              <div key={i} className="bg-surface-2 border border-neutral-800 rounded-lg p-6 hover:border-brass/30 transition-colors">
                <h3 className="text-base font-medium mb-2 text-brass">{f.title}</h3>
                <p className="text-sm text-neutral-400 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Live Museums */}
      <section id="live-museums" className="max-w-5xl mx-auto px-6 py-24">
        <p className="text-brass font-mono text-sm mb-3 tracking-widest uppercase">Live Museums</p>
        <h2 className="font-display text-3xl mb-8">Heritage health profiles</h2>

        {museums.length > 0 ? (
          <div className="grid gap-4">
            {museums.map((m: any) => (
              <Link
                key={m.slug}
                href={`/museum/${m.slug}`}
                className="bg-surface-2 border border-neutral-800 rounded-lg p-6 hover:border-brass/40 transition-all group"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-medium group-hover:text-brass transition-colors">{m.name}</h3>
                    <p className="text-sm text-neutral-500 mt-1">{m.location}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-neutral-400">{m.zone_count} zones</div>
                    <div className="text-xs text-neutral-600 mt-1">{m.total_readings?.toLocaleString()} readings</div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <p className="text-neutral-500">Connect to API to see live museums.</p>
        )}
      </section>

      {/* CTA */}
      <section className="border-t border-neutral-800 bg-surface-1">
        <div className="max-w-5xl mx-auto px-6 py-24 text-center">
          <h2 className="font-display text-3xl mb-4">Protect your heritage</h2>
          <p className="text-neutral-400 mb-8 max-w-xl mx-auto">
            Whether you&apos;re a world-class museum or a small community gallery,
            ConservaTwin gives you industrial-grade conservation monitoring for free.
          </p>
          <a href="https://github.com/Prithweeraj-Acharjee/conservatwin-platform" target="_blank" className="bg-brass text-surface-0 px-8 py-3 rounded font-medium hover:bg-brass/90 transition-colors inline-block">
            Get Started — It&apos;s Free
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-neutral-800 max-w-5xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between text-sm text-neutral-600">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-brass/40" />
            <span>ConservaTwin — MIT License</span>
          </div>
          <div>Built by <a href="https://prithwee.vercel.app" target="_blank" className="text-brass/60 hover:text-brass">Prithweeraj Acharjee</a></div>
        </div>
      </footer>
    </div>
  )
}
