/**
 * ESP32 Arduino Sketch — TCP Client
 * 
 * Connects to your Java server over Wi-Fi and sends a string every 5 seconds.
 * 
 * Board:   ESP32 (any variant)
 * Library: WiFi.h (built-in with ESP32 Arduino core)
 * 
 * Setup:
 *   1. Set WIFI_SSID / WIFI_PASSWORD to your network
 *   2. Set SERVER_IP to the machine running the Java service
 *   3. Set SERVER_PORT to match (default 5000)
 *   4. Flash, open Serial Monitor at 115200 baud
 */

#include <WiFi.h>

// ── Configuration ────────────────────────────────────────────
const char* WIFI_SSID     = "YOUR_SSID";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* SERVER_IP     = "192.168.1.100";   // IP of the Java server
const int   SERVER_PORT   = 5000;
const int   SEND_INTERVAL = 5000;              // ms between transmissions
// ─────────────────────────────────────────────────────────────

WiFiClient client;

void setup() {
    Serial.begin(115200);
    delay(500);

    Serial.print("Connecting to Wi-Fi: ");
    Serial.println(WIFI_SSID);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nWi-Fi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

void loop() {
    if (!client.connected()) {
        Serial.printf("Connecting to server %s:%d ...\n", SERVER_IP, SERVER_PORT);

        if (client.connect(SERVER_IP, SERVER_PORT)) {
            Serial.println("Connected to Java server.");
        } else {
            Serial.println("Connection failed. Retrying in 5s...");
            delay(SEND_INTERVAL);
            return;
        }
    }

    // ── Build your payload here ──────────────────────────────
    // Replace this with sensor readings, JSON, or any string.
    String payload = "Hello from ESP32! uptime=" + String(millis()) + "ms";
    // ─────────────────────────────────────────────────────────

    client.println(payload);   // println sends the string + newline (\n)
    Serial.println("Sent: " + payload);

    delay(SEND_INTERVAL);
}
