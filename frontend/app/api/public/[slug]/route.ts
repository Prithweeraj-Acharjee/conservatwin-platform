import { NextRequest, NextResponse } from 'next/server'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://conservatwin-platform.onrender.com'

export async function GET(request: NextRequest, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params

  // Retry up to 3 times (handles Render cold starts)
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const res = await fetch(`${API_BASE}/api/public/${slug}`, {
        signal: AbortSignal.timeout(50000),
        cache: 'no-store',
      })

      if (!res.ok) {
        return NextResponse.json({ error: 'Museum not found' }, { status: res.status })
      }

      const data = await res.json()
      return NextResponse.json(data)
    } catch {
      if (attempt === 2) {
        return NextResponse.json({ error: 'Backend unavailable' }, { status: 503 })
      }
      await new Promise(r => setTimeout(r, 2000))
    }
  }
}
