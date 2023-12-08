import socket

def receive_file(file_path, host, port):
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    try:
        # Receive file size
        file_size_str = client_socket.recv(1024).decode()
        file_size = int(file_size_str)
        print(f"Receiving file of size {file_size} bytes")

        # Receive file data
        with open(file_path, 'wb') as file:
            print("Receiving file...")
            total_received = 0
            while total_received < file_size:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
                total_received += len(data)
            print("File received successfully")

    finally:
        # Close the connection
        client_socket.close()

# Example usage
receive_file('C:/Users/khanh/Downloads/rec.pdf', '127.0.0.1', 12345)
