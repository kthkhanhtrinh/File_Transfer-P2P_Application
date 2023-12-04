
import socket
import threading

def handle_client(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[{addr}] {message}")
                response = f"Server received: {message}"
                client_socket.send(response.encode())
            else:
                break
        except:
            break
    client_socket.close()

def server_input():
    while True:
        cmd = input("Enter server command: ")
        # Here you can add code to process the server's command
        print(f"Server command entered: {cmd}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen()

    print("[STARTING] Server is starting...")
    input_thread = threading.Thread(target=server_input)
    input_thread.start()

    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

start_server()
