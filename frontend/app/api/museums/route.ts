import { NextResponse } from 'next/server'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://conservatwin-platform.onrender.com'

export async function GET() {
  try {
    const res = await fetch(`${API_BASE}/api/museums`, {
      signal: AbortSignal.timeout(9000),
      cache: 'no-store',
    })
    const data = await res.json()
    return NextResponse.json(data)
  } catch {
    return NextResponse.json({ museums: [] })
  }
}
