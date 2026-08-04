# echo_client.py
# Sends a message to an echo server and prints the response.

import socket


HOST = 'localhost'
PORT = 65432 # for sequential server, change to 65433 for threaded server
BUFFER_SIZE = 1024  # max bytes to receive at once


def run_echo_client():
    """Connect to the echo server, send a message, print the reply."""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        message = input("Enter a message to send: ")

        # Encode string to bytes before sending
        sock.sendall(message.encode('utf-8'))

        # Receive the echoed response
        data = sock.recv(BUFFER_SIZE)

        # Decode bytes back to string for display
        print(f"Echo received: {data.decode('utf-8')}")

    print("Connection closed.")


if __name__ == '__main__':
    run_echo_client()