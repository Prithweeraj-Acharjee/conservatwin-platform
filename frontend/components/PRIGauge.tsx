'use client'

export default function PRIGauge({ value, size = 120 }: { value: number; size?: number }) {
  const radius = (size - 16) / 2
  const circumference = Math.PI * radius
  const progress = Math.min(value / 100, 1)
  const offset = circumference * (1 - progress)

  const color = value < 20 ? '#4ade80'
    : value < 45 ? '#fbbf24'
    : value < 70 ? '#f97316'
    : '#ef4444'

  const label = value < 20 ? 'Stable'
    : value < 45 ? 'Elevated'
    : value < 70 ? 'High'
    : 'Critical'

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size / 2 + 16} viewBox={`0 0 ${size} ${size / 2 + 16}`}>
        {/* Background arc */}
        <path
          d={`M 8,${size / 2 + 8} A ${radius},${radius} 0 0 1 ${size - 8},${size / 2 + 8}`}
          fill="none"
          stroke="#2a2722"
          strokeWidth="8"
          strokeLinecap="round"
        />
        {/* Value arc */}
        <path
          d={`M 8,${size / 2 + 8} A ${radius},${radius} 0 0 1 ${size - 8},${size / 2 + 8}`}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={`${circumference}`}
          strokeDashoffset={offset}
          style={{ transition: 'stroke-dashoffset 1s ease, stroke 0.5s ease' }}
        />
        {/* Value text */}
        <text x={size / 2} y={size / 2} textAnchor="middle" fill={color} fontSize="24" fontFamily="JetBrains Mono" fontWeight="600">
          {value.toFixed(0)}
        </text>
        <text x={size / 2} y={size / 2 + 16} textAnchor="middle" fill="#8a8070" fontSize="10" fontFamily="Inter">
          PRI
        </text>
      </svg>
      <span className="text-xs mt-1 font-mono" style={{ color }}>{label}</span>
    </div>
  )
}
