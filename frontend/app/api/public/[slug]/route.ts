import { NextRequest, NextResponse } from 'next/server'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://conservatwin-platform.onrender.com'

export async function GET(request: NextRequest, { params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params

  try {
    const res = await fetch(`${API_BASE}/api/public/${slug}`, {
      signal: AbortSignal.timeout(9000),
      cache: 'no-store',
    })

    if (!res.ok) {
      return NextResponse.json({ error: 'Museum not found' }, { status: res.status })
    }

    const data = await res.json()
    return NextResponse.json(data)
  } catch {
    return NextResponse.json({ error: 'waking', message: 'Server is waking up...' }, { status: 503 })
  }
}
