import socket
import threading

def client_send2(s):
    while True:
        message = input("Client Send2: ")
        s.sendall(message.encode())

def client_recv1(s):
    while True:
        data = s.recv(1024)
        if data:
            print("Client Recv1:", data.decode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 12345))
    threading.Thread(target=client_send2, args=(s,)).start()
    client_recv1(s)
