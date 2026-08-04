# echo_server_simple.py
# Accepts one client connection at a time and echoes messages back.

import socket


HOST = 'localhost'
PORT = 65432
BUFFER_SIZE = 1024


def run_echo_server():
    """Start a simple iterative echo server."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Echo server running on {HOST}:{PORT}")
        print("Waiting for a client...\n")

        while True:
            # Block here until a client connects
            client_socket, client_address = server_socket.accept()
            print(f"Client connected: {client_address}")

            with client_socket:
                while True:
                    # Receive data (up to BUFFER_SIZE bytes)
                    data = client_socket.recv(BUFFER_SIZE)

                    if not data:
                        # Empty data means the client has disconnected
                        print(f"Client {client_address} disconnected.")
                        break

                    # Echo the data back unchanged
                    client_socket.sendall(data)
                    print(f"Echoed: {data.decode('utf-8')!r}")


if __name__ == '__main__':
    run_echo_server()