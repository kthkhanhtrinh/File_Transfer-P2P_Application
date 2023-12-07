import socket, os
import threading
data = None
public_path = None
client_open_port = None
# fetch_port = False
file_sent = False
# fetch_file = None

def listen_from_another_client(fname): # C1 listen from C2
    print("Port is opening, ready to connect peer!\n")
    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 12348))  # Bind to localhost and port 12345
        server_socket.listen()


        conn, addr = server_socket.accept()
        print(f'Have a connection from {addr}')
        data = conn.recv(1024).decode().strip()
        print(data)
        download_file(conn, fname)
        break

    print("Fetch port is close")



def connect_to_another_client(ip, fname, line):  # C2 connect to C1
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        peer_socket.connect((ip, 12348))  # Connect to the peer
        # peer_send_file(peer_socket, line)
        try: 
            peer_socket.send('hello from another client'.encode())
            peer_send_file(peer_socket, line)
            # print("Send to peer success")
        except: print("Send fail :((")
    # data = client_socket.recv(1024)
    except:
        print("Connect to", ip, "failed")
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

        s.sendall(msg.encode())
        
        if msg.startswith("fetch"):
            client_open_port = threading.Thread(target=listen_from_another_client, args=(fname,),)
            client_open_port.start()



def client_recv1(s):
    while True:
        data = s.recv(1024).decode().strip()
        print("received data:", data)

        if data.startswith("fetch fail"):
            _, fname = data.split("_")
            print(fname, "no such file founded!")
        
        # elif data == "Sending":
        #     # filename = s.recv(1024).decode().strip()
        #     download_file(s)
        elif data.startswith('fetch-request'):
            _, client_ip, fname, line = data.split("_")
            fetch_file = fname
            # print(client_ip)
            # print(fname)
            # print(line)
            threading.Thread(target=connect_to_another_client, args=(client_ip, fname, line)).start()
            # connect_to_another_client(client_ip, fname, line)
        
        # Server send to fetch request from another client
        else: 
            continue

def download_file(s, fetch_file):
    # print("Writing")
    try:
        # with open("C:\\Users\\Admin\\Downloads\\received-files.txt", "wb") as file:
        with open(f"C:\\Users\\khanh\\Downloads\\{fetch_file}", "wb") as file:
            data = s.recv(1024)
            # print(data)
            file.write(data)
            # print("File received successfully")
        file.close()
        print("File download success")
        # while(not file_sent):
        #     pass
        # fetch_port = False
    except Exception as e:
        print(f"Failed to open file: {e}")

def peer_send_file(conn, line):
    print("Sending")
    try: conn.send("Sending".encode())
    except: 
        print(f"Send to {conn} fail")
        return

    with open(line, 'rb') as file:
        data = file.read(1024)
        # print(data)
        while data:
            conn.send(data)
            data = file.read(1024)
    file.close()
    file_sent = True
    print("Send file successful")              
def peer_rev(s):
    data = s.recv(1024).decode().strip()
    if data == "Sending":
        download_file(s)

def check_valid_files(lname, fname):
    full_path = os.path.join(lname, fname)
    return os.path.isfile(full_path)

# server_ip = input("Enter server ip: ")
server_ip = '192.168.0.124'
# public_path = input("Enter download path: ")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server_ip, 12345))
    threading.Thread(target=client_send2, args=(s,)).start()
    client_recv1(s)
