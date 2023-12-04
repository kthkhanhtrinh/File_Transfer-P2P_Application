import socket
import threading

def server_send1(conn):
    while True:
        message = input("Server Send1: ")
        conn.sendall(message.encode())

def server_recv2(conn):
    while True:
        data = conn.recv(1024)
        if data:
            print("Server Recv2:", data.decode())

def handle_client(conn):
    threading.Thread(target=server_send1, args=(conn,)).start()
    
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 12345))
        s.listen()
        conn, addr = s.accept()
        with conn:
            thread = threading.Thread(target=handle_client, args=(conn, ))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

            server_recv2(conn)
