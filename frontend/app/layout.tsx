import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'ConservaTwin — Open-Source Heritage Preservation',
  description: 'Digital twin platform for cultural heritage preservation. Monitor environmental conditions, calculate preservation risk, and receive AI conservation recommendations.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}
