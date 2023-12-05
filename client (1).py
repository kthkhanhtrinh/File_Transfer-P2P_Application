import socket, os
import threading
data = None

client_open_port = None
fetch_port = False
file_sent = False

def listen_from_another_client(): # C1 listen from C2
    print("Port is opening, ready to connect peer!\n")
    while fetch_port:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 12346))  # Bind to localhost and port 12345
        server_socket.listen()


        conn, addr = server_socket.accept()
        print(f'Have a connection from {addr}')

        # with conn:
        #     print(f"Connected by {addr}")
        #     while True:
        #         data = conn.recv(1024)
        #         if not data:
        #             break
        #         conn.sendall(data)  # Echoes back the received data

    print("Fetch port is close")



def connect_to_another_client(ip, fname, line):  # C2 connect to C1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((ip, 12348))  # Connect to the peer
        peer_send_file(ip, line)
        # client_socket.sendall(b'hello from another client')
        # data = client_socket.recv(1024)

    # print(f'Received from another client: {data.decode()}')
    

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

        if msg == "Sending":
            download_file(s)

        s.sendall(msg.encode())
        if msg.startswith("fetch"):
            # client_open_port = threading.Thread(target=listen_from_another_client, args=(),)
            # client_open_port.start()
            fetch_port = True
            threading.Thread(target=listen_from_another_client, args=(),).start()
            # listen_from_another_client()


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
            _, client_ip, fname, line = data.split("_")
            threading.Thread(target=connect_to_another_client, args=(client_ip, fname, line)).start()
            # connect_to_another_client(client_ip, fname, line)
        
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
        while(not file_sent):
            pass
        fetch_port = False
    except Exception as e:
        print(f"Failed to open file: {e}")

def peer_send_file(conn, line):
    # print("Sending")
    conn.send("Sending".encode())
    filename = line[line.rfind("\'") + 1:]
    # conn.send(filename.encode())
    filename = filename[:-1]
    print(filename)
    with open(filename, 'rb') as file:
        data = file.read(1024)
        # print(data)
        while data:
            conn.send(data)
            data = file.read(1024)
    file.close()
    file_sent = True
    # print("Sending successful")              

def check_valid_files(lname, fname):
    full_path = os.path.join(lname, fname)
    return os.path.isfile(full_path)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # s.connect(('10.128.158.79', 12345))
    # s.connect(('localhost', 12345))
    s.connect(('192.168.0.124', 12345))
    threading.Thread(target=client_send2, args=(s,)).start()
    client_recv1(s)
