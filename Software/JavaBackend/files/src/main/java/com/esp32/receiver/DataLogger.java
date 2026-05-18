package com.esp32.receiver;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.logging.Logger;

/**
 * Thread-safe CSV logger that appends received data with timestamps.
 *
 * CSV format:
 *   timestamp, source_ip, data
 */
public class DataLogger {

    private static final Logger logger = Logger.getLogger(DataLogger.class.getName());
    private static final DateTimeFormatter TIMESTAMP_FMT =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    private final Path filePath;
    private final Object lock = new Object();

    public DataLogger(String fileName) throws IOException {
        this.filePath = Paths.get(fileName).toAbsolutePath();
        boolean isNew = !Files.exists(filePath);

        // Append mode — data survives server restarts
        try (PrintWriter writer = new PrintWriter(new FileWriter(filePath.toFile(), true))) {
            if (isNew) {
                // Write CSV header only for brand-new files
                writer.println("timestamp,source_ip,data");
            }
        }

        logger.info("DataLogger ready: " + filePath);
    }

    /**
     * Appends a single record to the CSV file.
     *
     * @param sourceIp the IP address of the sending ESP32
     * @param data     the raw string received
     */
    public void log(String sourceIp, String data) {
        String timestamp = LocalDateTime.now().format(TIMESTAMP_FMT);
        // Escape any commas or quotes inside the data field
        String safeData = escapeCsvField(data);

        synchronized (lock) {
            try (PrintWriter writer = new PrintWriter(new FileWriter(filePath.toFile(), true))) {
                writer.printf("%s,%s,%s%n", safeData);
            } catch (IOException e) {
                logger.severe("Failed to write data to CSV: " + e.getMessage());
            }
        }
    }

    public String getFilePath() {
        return filePath.toString();
    }

    // Wrap field in quotes if it contains a comma, quote, or newline
    private String escapeCsvField(String value) {
        if (value.contains(",") || value.contains("\"") || value.contains("\n")) {
            return "\"" + value.replace("\"", "\"\"") + "\"";
        }
        return value;
    }
}
