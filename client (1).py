import socket, os
import threading
data = None


def listen_from_another_client(): # C1 listen from C2
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12346))  # Bind to localhost and port 12345
    server_socket.listen()

    
    conn, addr = server_socket.accept()
    print(f'Have a connection from {addr}')

    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)  # Echoes back the received data


    pass


def connect_to_another_client(ip):  # C2 connect to C1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((ip, 12345))  # Connect to the server
        client_socket.sendall(b'hello from another client')
        data = client_socket.recv(1024)

    print(f'Received from another client: {data.decode()}')
    
    



def client_send2(s):
    while True:
        msg = input("Client command (publish/fetch): ")

        if not (msg.startswith("publish") or msg.startswith("fetch")):
            print("Error, enter again")
            if msg.startswith("quit"):
                s.close()
            continue
        
        if msg.startswith("publish"):
            #Check if valid file
            _, lname, fname = msg.split(" ")
            if check_valid_files(lname, fname):
                msg = f"publish_{lname}_{fname}"
            else:
                print("Invalid lname or fname")
                continue

        if msg.startswith("fetch"):
            _, fname = msg.split(" ")
            msg = f"fetch_{fname}"
            # try:
            #     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as u:
                    
            #         # msg = "Still coding please wait"
            #         #def open port
            #         # listen_from_another_client()

            # except Exception:
            #     print("Unable to get IP Address")


        s.sendall(msg.encode())


def client_recv1(s):
    while True:
        data = s.recv(1024).decode().strip()
        print("received data:", data)

        if data.startswith("fetch fail"):
            _, fname = data.split("_")
            print(fname, "no such file founded!")
        
        elif data == "Sending":
            # filename = s.recv(1024).decode().strip()
            download_file(s)
        elif data.startswith('fetch-request'):
            _, fname, client_ip = data.slipt("_")
            connect_to_another_client(client_ip)
            
        # Server send to fetch request from another client
        else: 
            continue

def download_file(s):
    # print("Writing")
    try:
        with open("C:\\Users\\khanh\\Downloads\\received-files.txt", "wb") as file:
            data = s.recv(1024)
            # print(data)
            file.write(data)
            # print("File received successfully")
        file.close()
    except Exception as e:
        print(f"Failed to open file: {e}")
              

def check_valid_files(lname, fname):
    full_path = os.path.join(lname, fname)
    return os.path.isfile(full_path)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # s.connect(('10.128.158.79', 12345))
    # s.connect(('localhost', 12345))
    s.connect(('192.168.0.124', 12345))
    threading.Thread(target=client_send2, args=(s,)).start()
    client_recv1(s)
