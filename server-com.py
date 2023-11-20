import socket
import threading
import pickle
import os

connected_clients = []
username = ""

def main():
    print("[STARTING] Server is starting...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '0.0.0.0'
    server_port = 12345
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_host}:{server_port}")
    client_info = {} 

    while True:
        client_socket, addr = server_socket.accept()
        client_address, client_port = addr
        print(f"Connection from {addr}")
        client_info[client_address] = client_address

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def user_register(client_socket, client_address):

    connected_clients.append((client_socket, client_address))

    username = client_socket.recv(1024).decode("utf-8").strip()
    password = client_socket.recv(1024).decode("utf-8").strip()

    print(f"Received new username: {username}, new password: {password}")

    user_acount_file = "users.txt"
    users_file_path = open("users.txt", "r")
    check = checkExitedAccount(username, password, users_file_path)
    users_file_path.close()
    
    if check:
        client_socket.send("FAILED".encode("utf-8"))
        return False 
    else: 
        with open(user_acount_file, "a") as file:
            file.write(f"{username}:{password}\n")
        # client_socket.send("Registration successful. You can now log in.".encode())
        
        client_socket.send("OK".encode("utf-8"))
        print("Registration successful")
        return True

def authenticate_client(client_socket):
    # Receive username and password separately
    username = client_socket.recv(1024).decode("utf-8").strip()
    password = client_socket.recv(1024).decode("utf-8").strip()
    
    # For debugging, print the received credentials
    #print(f"Received username: {username}, password: {password}")

    users_file = open("users.txt", "r")
    check = checkExitedAccount(username, password, users_file)
    users_file.close()
    # Check credentials
    if check:
        client_socket.send("OK".encode("utf-8"))
        return True
    
    else:
        client_socket.send("FAILED".encode("utf-8"))
        return False 

def checkExitedAccount(username, password, users_file):
    credentials = [line.strip().split(':') for line in users_file]
    
    for stored_username, stored_password in credentials:
        if username == stored_username and password == stored_password:
            return True

    return False

def receive_file(client_socket):
    with open('received_file.txt', 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            print("File received successfully")
            client_socket.close()

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    connected = True
    while connected:
        option = client_socket.recv(1024).decode("utf-8").strip()
        print(option.upper())
        
        if option == "login":
            if authenticate_client(client_socket):
                #todo input discover/ ping hostname -> thread
                # server_input(client_socket, client_address)
                #todo listen publish/ fetch from client -> thread
                server_listen(client_socket, client_address)
                connected = False

            else:
                print("Authentication failed. Closing connection.")
                client_socket.close()
        elif option == "register":
            user_register(client_socket, client_address)
            client_socket.close()
        
        connected = False
        

    client_socket.close()

def server_input(client_socket, client_address):
    server_command, hostname = input("Server command: ").split()

    if hostname != client_address:
        print("Wrong hostname\n")
        client_socket.close()
    
    if server_command == "discover":
        # client_socket.send("discover".encode())
        handle_server_discover()

        files_data = client_socket.recv(1024)
        files = pickle.loads(files_data)

        print("List of files in the directory:")

        for file in files:
            print(file)

    if server_command == "ping":
        handle_server_ping(client_socket, client_address)
        return
    
    if server_command == "quit":
        return


def server_listen(client_socket, client_address):
    client_command = client_socket.recv(1024).decode("utf-8").strip()

    if client_command == "publish":
        handle_client_publish(client_socket, client_address)
        server_listening(client_socket, client_address)


    if client_command == "fetch":
        print(client_command.upper())
        handle_client_fetch(client_socket) 

    client_socket.close()    


def handle_client_publish(client_socket, hostname):
    try:
        lname = client_socket.recv(1024).decode("utf-8").strip()
        fname = client_socket.recv(1024).decode("utf-8").strip()
        file_path = os.path.join("", "public", f"{hostname}_{username}_published.txt")
        print(lname, " ", fname)
        with open(file_path, "a") as file:
            file.write(lname + fname + "\n")

        print(f"Published file from {hostname}: {lname + fname}")
    except Exception as e:
        print(f"Error in handle_client_publish: {e}")

def handle_server_discover():
    try:
        folder_path = os.path.join("..", "public")
        if not os.path.exists(folder_path):
            print("No files published yet.")
            return

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                print(f"Contents of {filename}:")
                with open(file_path, "r") as file:
                    file_contents = file.read().strip()
                    print(file_contents if file_contents else "No contents", "\n")
            else:
                print(f"{filename} is not a file.")
    except Exception as e:
        print(f"Error in handle_server_discover: {e}")

def handle_server_ping(client_socket, client_address):
    client_socket.send("ping".encode())
    response = client_socket.recv(1024).decode()
    # if response == "pong":
    print(f"Ping response from client: {response}")
        # print("f{client_address} is connecting")
    

def handle_client_fetch(client_socket):
    fname = client_socket.recv(1024).decode()
    server_search_fname(client_socket, fname)

def server_search_fname(client_socket, fname):
    print("fname:", fname)
    folder_path = "C:\\Users\\khanh\\OneDrive - hcmut.edu.vn\\Documents\\SCHOOL MATERIAL\\1.Computer_Network\\Ass1\\public"
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # Open each file and check for the search string
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_number, line in enumerate(file, 1):
                    if fname in line:
                        print(f"String found in file: {os.path.basename(file_path)}, line: {line}")
                        client_socket.send("FOUND".encode())
                        client_socket.send(os.path.basename(file_path).encode())
                        client_socket.send(line.encode())
                        # Send file
                        server_send_file(client_socket, line)
                        return
    client_socket.send("FAIL".encode())

    # client_socket.send("")
    # print("File cannot found")
    
def server_send_file(client_socket, file_path):
    file_path = file_path[:-1]
    with open(file_path, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)
    print("File sent success")

def server_listening(client_socket, client_address):
    server_command, hostname = input("Server command: ").split()
    if hostname != client_address:
        return

    if server_command == "discover":
        # client_socket.send("discover".encode())
        handle_server_discover()
    

if __name__ == "__main__":
    main()