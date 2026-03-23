const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://conservatwin-platform.onrender.com';

export async function fetchPublicDashboard(slug: string) {
  const res = await fetch(`${API_BASE}/api/public/${slug}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Museum not found');
  return res.json();
}

export async function fetchMuseums() {
  const res = await fetch(`${API_BASE}/api/museums`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch museums');
  return res.json();
}

export async function registerMuseum(data: { name: string; slug: string; location?: string }) {
  const res = await fetch(`${API_BASE}/api/museums/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return res.json();
}

export interface ZoneData {
  zone: {
    id: number;
    name: string;
    description: string;
    material_type: string;
    targets: { temp: [number, number]; rh: [number, number] };
  };
  current: { temperature: number; humidity: number; timestamp: string };
  pri: {
    value: number;
    risk_level: string;
    factors: string[];
    trend: { pri_value: number; timestamp: string }[];
  };
  recommendations: {
    priority: string;
    action: string;
    reason: string;
    category: string;
  }[];
  recent_alerts: { severity: string; message: string; created_at: string }[];
  readings_24h: { temperature: number; humidity: number; timestamp: string }[];
}

export interface MuseumDashboard {
  museum: {
    id: number;
    name: string;
    slug: string;
    location: string;
    created_at: string;
  };
  zones: ZoneData[];
  overall_health: {
    average_pri: number;
    worst_pri: number;
    status: string;
    zones_at_risk: number;
  };
}
