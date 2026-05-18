package com.esp32.receiver;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.logging.Logger;

/**
 * TCP Server that listens for incoming connections from ESP32 devices
 * and saves the received string data to a CSV file.
 */
public class Esp32TcpServer {

    private static final Logger logger = Logger.getLogger(Esp32TcpServer.class.getName());

    private final int port;
    private final DataLogger dataLogger;
    private final ExecutorService threadPool;
    private volatile boolean running = false;

    public Esp32TcpServer(int port, String outputFile) throws IOException {
        this.port = port;
        this.dataLogger = new DataLogger(outputFile);
        this.threadPool = Executors.newCachedThreadPool();
    }

    public void start() throws IOException {
        running = true;
        logger.info("ESP32 TCP Server starting on port " + port);
        logger.info("Logging data to: " + dataLogger.getFilePath());

        try (ServerSocket serverSocket = new ServerSocket(port)) {
            logger.info("Server listening... waiting for ESP32 connections.");

            while (running) {
                Socket clientSocket = serverSocket.accept();
                String clientAddress = clientSocket.getInetAddress().getHostAddress();
                logger.info("New connection from: " + clientAddress);

                // Handle each ESP32 connection in its own thread
                threadPool.submit(new ClientHandler(clientSocket, dataLogger));
            }
        } finally {
            threadPool.shutdown();
            logger.info("Server stopped.");
        }
    }

    public void stop() {
        running = false;
    }

    public static void main(String[] args) throws IOException {
        int port = 5000;
        String outputFile = "esp32_data.csv";

        // Allow overrides via command-line args: <port> <output-file>
        if (args.length >= 1) port = Integer.parseInt(args[0]);
        if (args.length >= 2) outputFile = args[1];

        Esp32TcpServer server = new Esp32TcpServer(port, outputFile);

        // Graceful shutdown on Ctrl+C
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            logger.info("Shutdown signal received.");
            server.stop();
        }));

        server.start();
    }
}
