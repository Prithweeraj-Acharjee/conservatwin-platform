import { NextResponse } from 'next/server'

export const maxDuration = 60

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://conservatwin-platform.onrender.com'

export async function GET() {
  try {
    await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(55000), cache: 'no-store' })
  } catch {
    // warming up
  }

  try {
    const res = await fetch(`${API_BASE}/api/museums`, {
      signal: AbortSignal.timeout(15000),
      cache: 'no-store',
    })
    const data = await res.json()
    return NextResponse.json(data)
  } catch {
    return NextResponse.json({ museums: [] })
  }
}
