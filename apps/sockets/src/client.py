
import socket, threading
import sys
sys.path.append('../applications-of-aes') # path to aes

# local packages
from aes import AES
from apps.utils import load_encryption_key, load_chunks

HOST = "127.0.0.1"
PORT = 7700

class Client:
    def __init__(self, host: str, port: int, user_name: str) -> None:
        self.host = host
        self.port = port
        self.user_name = user_name

        self.aes = AES(load_encryption_key()) # aes object

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
            byte_data = bytes()
            data_chunks = load_chunks(data)
            for chunk in data_chunks:
                byte_data += self.aes.encrypt(chunk) # encrypts the data to send

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
                text_data = str()
                data_chunks = load_chunks(data)
                for chunk in data_chunks:
                    text_data += self.aes.decrypt(chunk)

                print(text_data)

def main():
    user_name = input("Enter name: ")

    client = Client(HOST, PORT, user_name)
    client.run()

if __name__ == "__main__":
    main()
