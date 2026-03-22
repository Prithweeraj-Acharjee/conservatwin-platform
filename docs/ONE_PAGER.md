# ConservaTwin — One-Page Overview
*Print this and bring it to museum meetings*

---

## ConservaTwin
### Open-Source Environmental Monitoring for Cultural Heritage

---

**THE PROBLEM**

95% of the world's museums and heritage sites lack continuous environmental monitoring. Temperature and humidity fluctuations cause gradual, invisible damage — cracking paint, foxing on manuscripts, mold on textiles, warping of wood panels. By the time damage is visible, it's often irreversible.

Commercial monitoring systems cost $10,000–$100,000+. Most institutions can't afford them.

---

**THE SOLUTION**

ConservaTwin is a free, open-source platform that turns a $5 sensor into an industrial-grade conservation monitoring system.

| Component | What it does | Cost |
|-----------|-------------|------|
| ESP32 + DHT22 sensor | Reads temperature & humidity every 30s | ~$5 |
| ConservaTwin Platform | Cloud dashboard, risk analysis, AI recommendations | Free |
| Public Dashboard | Live heritage health profile for your museum | Free |

---

**KEY FEATURES**

**Preservation Risk Index (PRI)**
A 0-100 score that quantifies environmental stress on your collection. Goes beyond simple threshold alarms — considers deviation, stability, and rate-of-change.

**Material-Aware AI Advisor**
Different recommendations for different materials. The system knows that oil paintings need 45-55% RH while photographs need to stay below 20°C. 10 material profiles built in.

**Anomaly Detection**
Catches sensor failures, HVAC degradation, humidity spikes, and temperature drift before they damage your collection.

**Public Heritage Dashboard**
A live web page showing your museum's conservation health. Demonstrates institutional commitment to preservation. Useful for grant applications and donor communications.

---

**HOW IT WORKS**

```
Sensor on wall → reads temp/humidity every 30 seconds
     ↓
Data sent via WiFi to ConservaTwin cloud
     ↓
PRI calculated → AI recommendations generated → Alerts sent
     ↓
Dashboard shows live status, trends, and conservation advice
```

---

**PILOT PROGRAM**

I'm offering a **free 2-week pilot** for your museum:

1. I install 2-3 sensors in selected galleries (no drilling, no wiring — battery + WiFi)
2. ConservaTwin monitors conditions for 2 weeks
3. I deliver a conservation environment report with findings and recommendations
4. You keep the sensors and platform access — forever, for free

---

**ABOUT**

Built by Prithweeraj Acharjee
Computer Science, University of Toledo
Specialization: Digital twins, computer vision, AI for conservation

Previous work:
- ConservaTwin PLC: PLC-driven museum digital twin with PID control and SCADA HMI
- Centriole Detection: Deep learning pipeline at The Ray Research Laboratory
- Bengali Fake News Detection: NLP ensemble achieving 82.43% accuracy

Website: https://prithwee.vercel.app
GitHub: https://github.com/Prithweeraj-Acharjee/conservatwin-platform

---

*ConservaTwin is MIT-licensed open-source software. No vendor lock-in. No subscription fees. Ever.*
