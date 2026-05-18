package com.esp32.receiver;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.logging.Logger;

/**
 * Handles a single ESP32 client connection.
 * Reads lines of text and passes them to the DataLogger.
 */
public class ClientHandler implements Runnable {

    private static final Logger logger = Logger.getLogger(ClientHandler.class.getName());

    private final Socket socket;
    private final DataLogger dataLogger;

    public ClientHandler(Socket socket, DataLogger dataLogger) {
        this.socket = socket;
        this.dataLogger = dataLogger;
    }

    @Override
    public void run() {
        String clientAddress = socket.getInetAddress().getHostAddress();

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(socket.getInputStream()))) {

            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (!line.isEmpty()) {
                    logger.info("[" + clientAddress + "] Received: " + line);
                    dataLogger.log(clientAddress, line);
                }
            }

        } catch (IOException e) {
            logger.warning("Connection error with " + clientAddress + ": " + e.getMessage());
        } finally {
            try {
                socket.close();
            } catch (IOException ignored) {}
            logger.info("Connection closed: " + clientAddress);
        }
    }
}
