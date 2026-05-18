# ESP32 TCP Receiver — Java Service

Listens for TCP connections from ESP32 devices and appends received strings to a CSV file.

## Project Structure

```
esp32-receiver/
├── pom.xml
├── esp32_client.ino                          ← ESP32 counterpart sketch
└── src/main/java/com/esp32/receiver/
    ├── Esp32TcpServer.java                   ← Entry point / TCP listener
    ├── ClientHandler.java                    ← Per-connection reader
    └── DataLogger.java                       ← Thread-safe CSV writer
```

## Requirements

- Java 11+
- Maven 3.6+

## Build

```bash
cd esp32-receiver
mvn package -q
```

This produces `target/esp32-receiver.jar`.

## Run

```bash
# Default: port 5000, output file esp32_data.csv
java -jar target/esp32-receiver.jar

# Custom port and output file
java -jar target/esp32-receiver.jar 6000 my_sensor_data.csv
```

## CSV Output

Data is appended to `esp32_data.csv` in the working directory:

```
timestamp,source_ip,data
2024-03-15 10:23:01,192.168.1.42,Hello from ESP32! uptime=5012ms
2024-03-15 10:23:06,192.168.1.42,Hello from ESP32! uptime=10024ms
```

- **Append mode** — existing data is never overwritten when the server restarts.
- **Thread-safe** — multiple ESP32 devices can connect simultaneously.
- **CSV escaping** — commas/quotes inside the data field are properly escaped.

## ESP32 Setup

1. Open `esp32_client.ino` in Arduino IDE.
2. Set `WIFI_SSID`, `WIFI_PASSWORD`, and `SERVER_IP` (the machine running this service).
3. Flash to your ESP32.
4. The ESP32 sends a line every 5 seconds via `client.println(...)`. Each `println` = one CSV row.

## Customising the Payload

In the `.ino` sketch, replace the `payload` string with your actual sensor data, e.g.:

```cpp
// Temperature + humidity example
String payload = "temp=" + String(temperature) + ",humidity=" + String(humidity);
```

On the Java side, no changes are needed — it stores whatever string it receives.
