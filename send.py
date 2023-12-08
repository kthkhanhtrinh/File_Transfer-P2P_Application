import os
import socket

def send_file(file_path, host, port):
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        # Wait for a connection
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        try:
            # Send file size
            file_size = os.path.getsize(file_path)
            client_socket.send(str(file_size).encode())

            # Send file data
            with open(file_path, 'rb') as file:
                print("Sending file...")
                data = file.read(1024)
                while data:
                    client_socket.send(data)
                    data = file.read(1024)
                print("File sent successfully")

        finally:
            # Close the connection
            
            break

    # Close the server socket
    server_socket.close()

# Example usage
send_file('C:/Users/khanh/OS.pdf', '127.0.0.1', 12345)
