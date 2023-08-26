
import socket, threading, json

class Server:
    def __init__(self, host: str, port: int, max_connections: int) -> None:
        self.host = host
        self.port = port
        self.max_connections = max_connections
        
        self.connected_users = {}

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self) -> None:
        """Starting method of the server."""
        self.connect()

        # opens when a client connects to the server
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_name = client_socket.recv(1024).decode()
            print(f"Client connected [{client_address}: {client_name}]")

            connected_message = "Connected:\n\t" + "\n\t".join(list(self.connected_users.values()))
            client_socket.send(connected_message.encode())
 
            self.connected_users[client_socket] = client_name # adds user to connected users

            thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            thread.start()

    def connect(self) -> None:
        """Turns the server on."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_connections)

        print(f"=====\nServer Live!\nHost: {self.host}\nPort: {self.port}\n=====\n")

    def handle_client(self, client_socket, client_address) -> None:
        """Handles the messages sent by the clients."""
        with client_socket:
            # Broadcast the join message to all connected clients
            client_name = self.connected_users[client_socket]
            for client in self.connected_users.keys():
                if client != client_socket:
                    client.send(f"[Server] {client_name} joined the server.".encode())

            while True:
                data = client_socket.recv(4096) # recieves text
                # allows the server to know when a client disconnects
                if not data:
                    break
                print(f"[{client_name}] {data}")
                # Send the received data to all connected clients except the sender
                for client in self.connected_users.keys():
                    if client != client_socket:
                        client.send(data) # message

            del self.connected_users[client_socket]
            print(f"Client disconnected [{client_address}]")

def main() -> None:
    server_data = json.load(open("apps/sockets/config.json")) # opens data from config
    # server object
    server = Server(server_data["Host"], server_data["Port"], 5)
    server.run()

if __name__ == "__main__":
    main()
