#include <WiFi.h>
#include <HTTPClient.h>
 
// -------- CONFIG --------
const char* WIFI_SSID = "Spionage SANH";
const char* WIFI_PASS = "13636425";
 
// Home Assistant HTTP Service URL für EIN
const char* HA_URL_ON  = "http://homeassistant.local:8123/api/services/switch/turn_on";
 
// Dein Long-Lived Access Token
const char* TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJiYjk3OWQ4MWEwZTE0MzA0ODI0YzUxNGE3MWJmYTAxMCIsImlhdCI6MTc3MDU3OTgzOCwiZXhwIjoyMDg1OTM5ODM4fQ.K2vNtDW-hpAHGgjo32FRAVZghfXalyEXfnjlKkowfDE";
 
// Shelly Entität
const char* ENTITY_ID = "switch.shellyoutdoorsg3_e4b063dc9c2c";
// ------------------------
 
void turnOnShelly();
void setup() {
  Serial.begin(115200);
 
  // WLAN verbinden
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Verbinde WLAN");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWLAN verbunden ✅");
 
  // Shelly einschalten
  turnOnShelly();
}
 
void loop() {
  // nichts nötig
}
 
void turnOnShelly() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WLAN nicht verbunden ❌");
    return;
  }
 
  HTTPClient http;
  http.begin(HA_URL_ON);
  http.addHeader("Authorization", String("Bearer ") + TOKEN);
  http.addHeader("Content-Type", "application/json");
 
  // JSON Payload für Home Assistant Service
  String payload = "{\"entity_id\":\"" + String(ENTITY_ID) + "\"}";
 
  int httpResponseCode = http.POST(payload);
 
  if (httpResponseCode > 0) {
    Serial.print("HTTP Response Code: ");
    Serial.println(httpResponseCode);
    Serial.println("Shelly EIN gesendet ✅");
  } else {
    Serial.print("Fehler beim HTTP POST: ");
    Serial.println(httpResponseCode);
  }
 
  http.end();
}
