import socket, os
import threading

# Dictionary to keep track of client connections using their IP as key
client_connections = {}
public_path = "C:\\Users\\khanh\\OneDrive - hcmut.edu.vn\\Documents\\SCHOOL MATERIAL\\1.Computer_Network\\Ass1\\public"


def server_input(): # ping/discover
    while True:
        command = input("Server command (discover/ ping) hostname:")
        
        if command == 'quit':
            break

        if not (command.startswith("ping") or command.startswith("discover")):
            print("Error command, enter again")
            # if command.startswith("quit"):
            #     break
            continue
        
        command, ip = command.split(" ")
        
        if command == "discover":
            folder_path = public_path
            
            for filename in os.listdir(folder_path):
                # print(filename)
                if filename.startswith(ip):
                    full_path = os.path.join(folder_path, filename)
                    
                    with open(full_path, "r") as file:
                        file_contents = file.read().strip()
                        print(file_contents if file_contents else "No contents", "\n")
                    
                    continue  # Assuming you want to stop after finding the first file
                else: 
                    print("No file published yet from", ip)

        if command == "ping":
            if (checkOnline(ip)):
                print(f"{ip} still in connection")
            else:
                print(f"{ip} offline")
        
def checkOnline(ip):
    if ip in client_connections:
        return True
    else: 
        return False


def server_recv(conn, ip): #publish/fetch server know who send command to the server
    while True:
        try:
            data = conn.recv(1024).decode("utf-8").strip()
            
            if data.startswith("publish"):
                _, lname, fname = data.split("_")
                file_path = os.path.join(public_path, f"{ip}_published.txt")
                with open(file_path, "a") as file:
                    file.write(lname + fname + '\n')
                print(f"Published file from {ip}: {lname + fname}")
                
            if data.startswith("fetch"):
                _, fname = data.split("_")
                print(f"{ip} need {fname}")
                data = search_fname(conn, fname)
                peer_ip, line = data.split("_")
                print(f"Peer store that file: {peer_ip}")

                #check peer2 not alive
                if not checkOnline(peer_ip):
                    conn.send(f"fetch fail_{fname}".encode()) 
                    continue
                    
                
                msg = f"fetch-request_{ip}_{fname}_{line}"
                # server_send()
                #if peer2 is alive → send c2
                server_send(client_connections[peer_ip], msg)

        except ConnectionResetError:
            break

    del client_connections[ip]
    print(f"Client {ip} disconnected")

def server_send(conn, msg):
    conn.send(msg.encode())
    # pass

def search_fname(conn, fname): #conn → ip from fetch request client
    
    folder_path = public_path
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # print(f"String found in file: {file_path}")

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    if fname in line:
                        peer_ip, _ = os.path.basename(file_name).split("_")
                        # print(line)
                        # print(f"Peer store that file: {peer_ip}") #c2
                        return f"{peer_ip}_{line}"

    print("Found not thing")
    # 
    # conn.send(f"fetch fail_{fname}".encode()) 
   #  client_connections[ip] = conn
                        
                        

def server_send_file(conn, file_path, line):
    # print("Sending")
    conn.send("Sending".encode())
    # filename = line[line.rfind("\'") + 1:]
    # conn.send(filename.encode())
    # filename = filename[:-1]
    # print(filename)
    with open(line, 'rb') as file:
        data = file.read(1024)
        # print(data)
        while data:
            conn.send(data)
            data = file.read(1024)
    file.close()
    # print("Sending successful")


def handle_client(conn, addr):
    ip = addr[0]
    print(f'Connected to {addr}')
    client_connections[ip] = conn
    # Thread for receiving messages from this client
    threading.Thread(target=server_recv, args=(conn, ip), daemon=True).start()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 12345))
        s.listen()
        print("Server is listening on localhost:12345")
        # Start a thread for the server_send function
        threading.Thread(target=server_input, daemon=True).start()
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()

start_server()


