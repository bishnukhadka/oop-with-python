# daytime_client.py
# Connects to the daytime server and prints the current time.

import socket

HOST = 'localhost'
PORT = 17000

def get_server_time():
    """Connect to the daytime server and print the response."""

    # 1. Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        # 2. Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        # 3. Receive the response (up to 1024 bytes)
        data = client_socket.recv(1024)

        # 4. Decode bytes to string and display
        print(f"Server time: {data.decode('utf-8').strip()}")
    # client_socket closes automatically here

if __name__ == '__main__':
    get_server_time()