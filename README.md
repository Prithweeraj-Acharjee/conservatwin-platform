<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:1f6feb&height=200&section=header&text=ConservaTwin%20Platform&fontSize=38&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Open-Source%20Digital%20Twin%20for%20Heritage%20Conservation&descSize=16&descAlignY=55" width="100%" />

[![Live Demo](https://img.shields.io/badge/Live_Demo-conservatwin--platform.vercel.app-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://conservatwin-platform.vercel.app)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)]()
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)]()
[![IoT](https://img.shields.io/badge/IoT-ESP32-E7352C?style=for-the-badge&logo=espressif&logoColor=white)]()

</div>

---

## About

**ConservaTwin** is an open-source digital twin platform for cultural heritage preservation. Museums, temples, and historical buildings deteriorate because environmental conditions go unmonitored. Big institutions spend millions on climate control, but 95% of heritage sites have nothing.

**Our solution:** $5 sensors + free software = any museum can monitor and protect their collection.

---

## Features

- **Multi-Tenant Museum Management** - manage multiple sites from a single dashboard
- **Preservation Risk Index (PRI) Engine** - quantifies long-term environmental stress on artifacts
- **AI Conservation Advisor** - intelligent recommendations based on material-specific risk profiles
- **$5 IoT Sensor Integration** - ESP32 + DHT22 sensors for temperature and humidity monitoring
- **Anomaly Detection** - real-time alerts when conditions deviate from safe ranges
- **Material-Aware Risk Profiling** - different risk thresholds for oil paintings, textiles, metals, etc.

---

## Architecture

```
IoT Sensors (ESP32 + DHT22)
        |
        v
  FastAPI Backend
   |          |
   v          v
PRI Engine   AI Advisor
        |
        v
  Next.js Frontend
   |          |
   v          v
Dashboard   Alerts
```

---

## Tech Stack

<div align="center">

| Category | Technology |
|----------|-----------|
| **Backend** | Python, FastAPI |
| **Frontend** | Next.js, React, TypeScript |
| **IoT Hardware** | ESP32, DHT22 |
| **AI/ML** | Conservation risk models |
| **Database** | PostgreSQL |
| **Deployment** | Vercel |

</div>

---

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- ESP32 board with DHT22 sensor (optional for hardware integration)

### Installation

```bash
# Clone the repository
git clone https://github.com/Prithweeraj-Acharjee/conservatwin-platform.git
cd conservatwin-platform

# Backend setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend setup (in a new terminal)
cd frontend
npm install
npm run dev
```

---

## IoT Sensor Setup

Total hardware cost: **~$5**

| Component | Cost |
|-----------|------|
| ESP32 Dev Board | ~$3 |
| DHT22 Sensor | ~$2 |

The sensor reads temperature and humidity every 30 seconds and transmits data to the platform via WiFi.

---

## Author

**Prithweeraj Acharjee Porag**

[![GitHub](https://img.shields.io/badge/GitHub-Prithweeraj--Acharjee-181717?style=flat-square&logo=github)](https://github.com/Prithweeraj-Acharjee)
[![Portfolio](https://img.shields.io/badge/Portfolio-prithwee.vercel.app-000000?style=flat-square&logo=vercel)](https://prithwee.vercel.app)

---

## License

This project is open source and available under the [MIT License](LICENSE).

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:1f6feb&height=100&section=footer" width="100%" />
</div>
