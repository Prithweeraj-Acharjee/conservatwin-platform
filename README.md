# ConservaTwin Platform

**Open-source digital twin for cultural heritage preservation.**

Museums, temples, and historical buildings are slowly deteriorating because environmental conditions aren't monitored. Big institutions spend millions on climate control — but 95% of the world's heritage sites have nothing.

ConservaTwin changes that. A **$5 sensor** plugged into a wall sends temperature and humidity data to this free platform, which calculates preservation risk and provides AI-powered conservation recommendations.

**Think: a medical chart for buildings and art — anyone can see it, researchers can study it, conservators can act on it.**

---

## How It Works

```
ESP32 + DHT22 sensor ($5)
        │
        ▼  POST every 30s
┌───────────────────────┐
│  ConservaTwin API     │
│  ┌─────────────────┐  │
│  │ PRI Engine      │  │  ← Preservation Risk Index
│  │ Anomaly Detect  │  │  ← Spike/flatline/drift detection
│  │ AI Advisor      │  │  ← Material-specific recommendations
│  └─────────────────┘  │
└───────────┬───────────┘
            ▼
    Public Dashboard
    (anyone can view)
```

## Features

- **Multi-tenant** — any museum registers and adds their zones
- **Preservation Risk Index (PRI)** — quantifies environmental stress (0-100)
- **Material-aware** — different risk profiles for oil paintings, textiles, paper, wood, metal, ceramics, photographs
- **AI Conservation Advisor** — actionable recommendations based on conditions and material type
- **Anomaly detection** — flags sensor spikes, flatlines, drift, and impossible values
- **Public heritage dashboard** — transparent conservation data for any museum
- **$5 hardware** — ESP32 + DHT22, Arduino sketch included
- **Free to deploy** — Render (API) + Vercel (frontend), all free tier

## Quick Start

### 1. Run locally

```bash
pip install -r backend/requirements.txt

# Seed demo data
python -m backend.demo_seed

# Start server
uvicorn backend.main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive API.

### 2. Register a museum

```bash
curl -X POST http://localhost:8000/api/museums/register \
  -H "Content-Type: application/json" \
  -d '{"name": "My Museum", "slug": "my-museum", "location": "My City"}'
```

Save the API key from the response.

### 3. Add a zone

```bash
curl -X POST http://localhost:8000/api/museums/my-museum/zones \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Main Gallery",
    "material_type": "oil_painting",
    "target_temp_min": 19, "target_temp_max": 22,
    "target_rh_min": 45, "target_rh_max": 55
  }'
```

### 4. Send sensor data

```bash
curl -X POST http://localhost:8000/api/sensors/reading \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -d '{"zone_id": 1, "temperature": 23.5, "humidity": 62.0}'
```

Response includes real-time PRI, risk level, and any anomalies detected.

### 5. View public dashboard

```
GET http://localhost:8000/api/public/my-museum
```

Returns complete museum health profile with all zones, PRI trends, recommendations, and alerts.

## Hardware Setup ($5)

| Component | Cost | Purpose |
|-----------|------|---------|
| ESP32 dev board | ~$3 | WiFi microcontroller |
| DHT22 sensor | ~$2 | Temperature + humidity |

Wire DHT22 data pin to GPIO 4, upload `hardware/esp32_sensor.ino` with your WiFi and API credentials. That's it.

## Material Profiles

The PRI engine adjusts risk calculations based on what's being preserved:

| Material | Temp Sensitivity | Humidity Sensitivity | Slew Tolerance |
|----------|-----------------|---------------------|----------------|
| Oil painting | High | Very High | Low |
| Watercolor | Medium | Very High | Very Low |
| Textile | Low | Very High | Low |
| Paper | Medium | Very High | Very Low |
| Photograph | Very High | Very High | Very Low |
| Wood | Medium | Very High | Low |
| Metal | Very High | High | Medium |
| Ceramic | Low | Low | High |
| Stone | Very Low | Medium | High |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/museums/register` | Register a new museum |
| GET | `/api/museums` | List all public museums |
| GET | `/api/museums/{slug}` | Get museum details and zones |
| POST | `/api/museums/{slug}/zones` | Add a zone |
| POST | `/api/sensors/reading` | Ingest a sensor reading |
| POST | `/api/sensors/batch` | Ingest multiple readings |
| GET | `/api/public/{slug}` | Public dashboard data |

## Architecture

```
backend/
├── main.py              # FastAPI application
├── database.py          # SQLite multi-tenant database
├── demo_seed.py         # Demo data generator
├── routes/
│   ├── museums.py       # Museum & zone management
│   ├── sensors.py       # IoT data ingestion + analysis
│   ├── public.py        # Public dashboard API
│   └── auth.py          # API key authentication
├── engine/
│   ├── pri.py           # Preservation Risk Index calculator
│   ├── advisor.py       # AI conservation recommendations
│   └── anomaly.py       # Anomaly detection
hardware/
└── esp32_sensor.ino     # Arduino sketch for ESP32 + DHT22
```

## Deploy (Free)

**Backend → Render.com**
1. Push to GitHub
2. Connect repo to Render
3. It auto-detects the `render.yaml` config
4. Deploy (free tier)

**Frontend → Vercel** (coming soon)

## Roadmap

- [ ] Next.js frontend dashboard
- [ ] Real-time WebSocket updates
- [ ] Photo-based degradation detection (computer vision)
- [ ] Predictive risk modeling (ML)
- [ ] Multi-language support
- [ ] Mobile app for conservators
- [ ] Public heritage health map

## Why This Matters

UNESCO estimates that billions in cultural heritage is deteriorating worldwide. Most heritage sites — especially in developing countries — lack basic environmental monitoring.

ConservaTwin makes conservation technology accessible to every museum, temple, church, and historical building on Earth. For $5 in hardware and free software.

## Author

Built by **Prithweeraj Acharjee** — artist, engineer, and CSE student at the University of Toledo.

Conservation is engineering. Heritage is data. Preservation is open-source.

## License

MIT — use it, fork it, save some heritage.
