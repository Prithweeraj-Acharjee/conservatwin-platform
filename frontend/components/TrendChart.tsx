'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'

interface Reading {
  temperature: number
  humidity: number
  timestamp: string
}

export default function TrendChart({
  readings,
  tempRange,
  rhRange,
}: {
  readings: Reading[]
  tempRange: [number, number]
  rhRange: [number, number]
}) {
  const data = readings.map((r, i) => ({
    idx: i,
    time: new Date(r.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    temp: r.temperature,
    rh: r.humidity,
  }))

  return (
    <div className="bg-surface-2 border border-neutral-800 rounded-lg p-4">
      <div className="text-[10px] font-mono uppercase text-neutral-500 mb-3">24h Environmental Trend</div>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2722" />
          <XAxis dataKey="time" tick={{ fontSize: 9, fill: '#6b6560' }} interval="preserveStartEnd" />
          <YAxis yAxisId="temp" tick={{ fontSize: 9, fill: '#6b6560' }} domain={['auto', 'auto']} />
          <YAxis yAxisId="rh" orientation="right" tick={{ fontSize: 9, fill: '#6b6560' }} domain={['auto', 'auto']} />
          <Tooltip
            contentStyle={{ background: '#1a1816', border: '1px solid #2a2722', borderRadius: '6px', fontSize: '11px' }}
            labelStyle={{ color: '#8a8070' }}
          />
          <ReferenceLine yAxisId="temp" y={tempRange[0]} stroke="#4ade80" strokeDasharray="4 4" strokeOpacity={0.3} />
          <ReferenceLine yAxisId="temp" y={tempRange[1]} stroke="#4ade80" strokeDasharray="4 4" strokeOpacity={0.3} />
          <Line yAxisId="temp" type="monotone" dataKey="temp" stroke="#f97316" strokeWidth={1.5} dot={false} name="Temp °C" />
          <Line yAxisId="rh" type="monotone" dataKey="rh" stroke="#60a5fa" strokeWidth={1.5} dot={false} name="RH %" />
        </LineChart>
      </ResponsiveContainer>
      <div className="flex gap-4 mt-2 justify-center">
        <span className="text-[10px] text-neutral-500 flex items-center gap-1">
          <span className="w-3 h-0.5 bg-orange-500 inline-block" /> Temperature
        </span>
        <span className="text-[10px] text-neutral-500 flex items-center gap-1">
          <span className="w-3 h-0.5 bg-blue-400 inline-block" /> Humidity
        </span>
        <span className="text-[10px] text-neutral-500 flex items-center gap-1">
          <span className="w-3 h-px bg-green-400 inline-block border-t border-dashed border-green-400" /> Target range
        </span>
      </div>
    </div>
  )
}
