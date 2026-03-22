/*
 * ConservaTwin — ESP32 Sensor Node
 * Reads temperature & humidity from DHT22 sensor
 * Posts data to ConservaTwin Platform API every 30 seconds
 *
 * Hardware needed (~$5 total):
 *   - ESP32 dev board ($3)
 *   - DHT22 sensor ($2)
 *   - Wiring: DHT22 data pin → GPIO 4, VCC → 3.3V, GND → GND
 *
 * Setup:
 *   1. Install Arduino IDE
 *   2. Add ESP32 board support
 *   3. Install "DHT sensor library" by Adafruit
 *   4. Set your WiFi credentials, API key, and zone ID below
 *   5. Upload to ESP32
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// ===== CONFIGURE THESE =====
const char* WIFI_SSID     = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD  = "YOUR_WIFI_PASSWORD";
const char* API_URL        = "https://your-conservatwin-api.onrender.com/api/sensors/reading";
const char* API_KEY        = "ct_YOUR_API_KEY_HERE";
const int   ZONE_ID        = 1;
const int   SEND_INTERVAL  = 30000;  // 30 seconds
// ============================

#define DHT_PIN  4
#define DHT_TYPE DHT22

DHT dht(DHT_PIN, DHT_TYPE);
unsigned long lastSend = 0;

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Connect to WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected! IP: " + WiFi.localIP().toString());
}

void loop() {
  if (millis() - lastSend < SEND_INTERVAL) return;
  lastSend = millis();

  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("ERROR: Failed to read from DHT22 sensor");
    return;
  }

  Serial.printf("Temp: %.1f°C  Humidity: %.1f%%\n", temp, hum);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("X-Api-Key", API_KEY);

    String payload = "{\"zone_id\":" + String(ZONE_ID) +
                     ",\"temperature\":" + String(temp, 1) +
                     ",\"humidity\":" + String(hum, 1) + "}";

    int responseCode = http.POST(payload);

    if (responseCode > 0) {
      String response = http.getString();
      Serial.printf("Sent! Response (%d): %s\n", responseCode, response.c_str());
    } else {
      Serial.printf("Send failed: %s\n", http.errorToString(responseCode).c_str());
    }

    http.end();
  } else {
    Serial.println("WiFi disconnected, reconnecting...");
    WiFi.reconnect();
  }
}
