# echo_server_threaded.py
# Handles multiple clients simultaneously using threads.

import socket
import threading


HOST = 'localhost'
PORT = 65433
BUFFER_SIZE = 1024


def handle_client(client_socket, client_address):
    """
    Handle one client connection in its own thread.
    This function runs independently for every connected client.
    """
    print(f"[Thread] Serving {client_address}")

    with client_socket:
        while True:
            try:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                client_socket.sendall(data)
                print(f"[{client_address}] Echoed: {data.decode('utf-8')!r}")
            except ConnectionResetError:
                break

    print(f"[Thread] {client_address} disconnected.")


def run_threaded_server():
    """Start a threaded echo server that handles multiple clients at once."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        print(f"Threaded echo server on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # Create a new thread for each client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True      # thread exits when main program exits
            )
            client_thread.start()
            print(f"Active threads: {threading.active_count() - 1}")


if __name__ == '__main__':
    run_threaded_server()