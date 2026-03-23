import { NextResponse } from 'next/server'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://conservatwin-platform.onrender.com'

export async function GET() {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const res = await fetch(`${API_BASE}/api/museums`, {
        signal: AbortSignal.timeout(50000),
        cache: 'no-store',
      })
      const data = await res.json()
      return NextResponse.json(data)
    } catch {
      if (attempt === 2) {
        return NextResponse.json({ museums: [] })
      }
      await new Promise(r => setTimeout(r, 2000))
    }
  }
}
