# Socket Chat Application

This is a simple socket-based chat application consisting of a server and client script. The server allows multiple clients to connect and exchange messages securely using AES encryption.

## Features

- Real-time chat functionality over a local network.
- AES encryption for secure message transmission.
- Server supports multiple clients concurrently.
- User-friendly command-line interface.

## Getting Started

### Prerequisites

- Applications of AES repository (larger repository).

## Usage

Before running the Socket Chat Application, make sure you have the "Applications of AES" repository cloned and accessible, as it contains required modules.

1. **Configuration**: 

   Both the server and client use a `config.json` file to store their configuration options. Edit this file to customize host, port, and other settings. Encryption keys are managed automatically within the application.

2. **Run the server script**:

   ```bash
   python server.py
   ```

   The server will start and wait for incoming connections. Once the server is running, you can proceed to run the client(s).

3. **Run the client script**:

   ```bash
   python client.py
   ```

   When prompted, enter your desired username. The client script will connect to the server and provide a command-line interface for sending and receiving messages.

5. **Output**:

   - **Server**:

     ```
     =====
     Server Live!
     Host: <your-host>
     Port: <your-port>
     =====
     ```

     The server's console will display information about the server's status, including the host and port it's listening on.

   - **Client**:

     ```
     =====
     Connected to server!
     Host: <server-host>
     Port: <server-port>
     Strength: <key-length>
     <connected-message>
     =====
     ```

     The client's console will show that it's connected to the server, displaying the server's host, port, encryption key strength, and a connected message.

6. **Interaction**:

   - To send a message, type your message and press Enter.
   - To exit the client, type "exit" and press Enter.


## Configuration

- Both the server and client use a `config.json` file to store their configuration options. Make sure to edit this file to customize host, port, and other settings.
- Encryption keys are managed automatically within the application.
