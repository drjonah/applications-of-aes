
import socket, threading, json
import sys
sys.path.append('../applications-of-aes') # path to aes

# local packages
from aes import AES
from apps.utils import load_encryption_settings

class Client:
    def __init__(self, host: str, port: int, user_name: str) -> None:
        self.host = host
        self.port = port
        self.user_name = user_name

        self.key, self.cbc, self.iv = load_encryption_settings() # load encryption settings
        self.aes = AES(self.key) # aes object

        self.client_socket = socket.socket()

    def run(self) -> None:
        """This starts the thread for the client."""
        self.connect()

        receive_thread = threading.Thread(target=self.receive_messages) # client listens for messages
        receive_thread.start()

        self.send_messages()

        self.client_socket.close()

    def connect(self) -> None:
        """This connects the client to the server."""
        self.client_socket.connect((self.host, self.port))
        self.client_socket.send(self.user_name.encode())

        connected_message = self.client_socket.recv(4096).decode()

        print(f"=====\nConnected to server!\nHost: {self.host}\nPort: {self.port}\nStrength: {len(self.aes.key)}\n{connected_message}\n=====\n")

    def send_messages(self) -> None:
        """Sends and encrypts messages to server."""
        while True:
            data_input = input() # client input

            # checks to see if user wants to disconnect
            if data_input == "exit":
                break
            data = f"[{self.user_name}] {data_input}" # adds username to encryption

            # encrypts the data to send
            byte_data = self.aes.encrypt(data, self.cbc, self.iv)

            self.client_socket.send(byte_data)

    def receive_messages(self) -> None:
        """Receive and display messages from the server."""
        while True:
            # recieve
            data = self.client_socket.recv(4096)
            
            # checks to see if data is empty
            if not data:
                break

            # check to see if its a join message
            if b"[Server]" in data:
                print(data.decode())
            else:
                # decrypts the data from the user
                text_data = self.aes.decrypt(data, self.cbc, self.iv)

                print(text_data)

def main():
    user_name = input("Enter name: ")
    server_data = json.load(open("apps/sockets/config.json")) # opens data from config
    # client object
    client = Client(server_data["Host"], server_data["Port"], user_name)
    client.run()

if __name__ == "__main__":
    main()
