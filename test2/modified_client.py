
import socket
import threading

def listen_to_server(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Message from server: {message}")
            else:
                break
        except:
            break

def send_to_server(client_socket):
    while True:
        message = input("Enter your message: ")
        client_socket.send(message.encode())

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    listen_thread = threading.Thread(target=listen_to_server, args=(client_socket,))
    send_thread = threading.Thread(target=send_to_server, args=(client_socket,))

    listen_thread.start()
    send_thread.start()

    listen_thread.join()
    send_thread.join()

if __name__ == "__main__":
    start_client()
