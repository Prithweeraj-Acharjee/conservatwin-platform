import { NextRequest, NextResponse } from 'next/server'

export const maxDuration = 60

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://conservatwin-platform.onrender.com'

export async function GET(request: NextRequest, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params

  // First, wake up Render if it's sleeping
  try {
    await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(55000), cache: 'no-store' })
  } catch {
    // Ignore - just warming up
  }

  // Now fetch the actual data
  try {
    const res = await fetch(`${API_BASE}/api/public/${slug}`, {
      signal: AbortSignal.timeout(15000),
      cache: 'no-store',
    })

    if (!res.ok) {
      return NextResponse.json({ error: 'Museum not found' }, { status: res.status })
    }

    const data = await res.json()
    return NextResponse.json(data)
  } catch {
    return NextResponse.json({ error: 'Backend is starting up. Please refresh in 30 seconds.' }, { status: 503 })
  }
}
