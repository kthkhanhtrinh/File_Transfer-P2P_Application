import socket
import pickle
import os
import threading, time

username = ""
input_thread = None
listen_thread = None

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '127.0.0.1' #change to your IP addrs
    # server_host = '172.20.10.4'
    server_port = 12345

    client_socket.connect((server_host, server_port))
    while True:
        option = input("Select option (login/register): ")
        client_socket.send(option.encode())

        if (option == "login"):
            if authenticate_client(client_socket):
                input_thread = threading.Thread(target=client_input, args=(client_socket, ))
                input_thread.start()
                client_listen(client_socket)
            else:
                print("Authentication failed. Exiting.")
        
        elif (option == "register"):
            if user_register(client_socket):
                print("Register successfully")
            else:
                print("Register failed. Exiting")
        
        elif (option == "quit"):
            break

        else:
            print("Invalid command!")

    client_socket.close()

def client_listen(client_socket):
    # while True:
    server_command = client_socket.recv(1024).decode("utf-8").strip()

    if server_command == "discover":
        directory = "..\\public"
        files = list_files(directory)
        files_data = pickle.dumps(files)
        client_socket.send(files_data)

    elif server_command == "ping":
        client_socket.send("ping".encode())
        print("Ping request received. Pinging back to the server.")
    
    elif server_command == "quit":
        return
    
    else: 
        pass
        

def client_input(client_socket):
    client_command = input("1.publish lname fname\n2.fetch fname\nEnter command: ")
    # client_command, lname, fname = client_command.split(" ")
    if client_command.startswith("publish"):
        client_command, lname, fname = client_command.split(" ")
        client_socket.send(client_command.encode())
        handle_client_publish(client_socket, client_command, lname, fname)

    if client_command.startswith("fetch"):
        client_command, fname = client_command.split(" ")
        client_socket.send(client_command.encode())
        handle_client_fetch(client_socket, fname)


def user_register(client_socket):
    username = input("Enter new username: ")
    password = input("Enter new password: ")

    client_socket.send(username.encode())
    client_socket.send(password.encode()) 
    # client_socket.close()
    response = client_socket.recv(1024).decode().strip()
    return response == "OK" 

def authenticate_client(client_socket):
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Send username and password separately
    client_socket.send(username.encode())
    client_socket.send(password.encode())

    # Receive authentication response
    response = client_socket.recv(1024).decode().strip()
    return response == "OK"

def send_file(client_socket):
    file_path = 'sending-file.txt'
    with open(file_path, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)
            
    print("File sent successfully")

def handle_client_publish(client_socket, client_command, lname, fname):
    if check_valid_files(lname, fname):

        client_socket.send(lname.encode())
        client_socket.send(fname.encode())
    else:
        print("Wrong lname or fname, please check again")
        

def handle_client_fetch(client_socket, fname):
    client_socket.send(fname.encode())
    if(client_socket.recv(1024).decode() == "FOUND"):
        file_path = client_socket.recv(1024).decode()
        file_dir = client_socket.recv(1024).decode()
        base_fname = os.path.basename(file_path)
        target_name, user, file = base_fname.split("_")
        start_download_file(client_socket, target_name, fname)
        print(target_name)
    
def start_download_file(client_socket, target_name, fname):
    with open("received-file.txt", 'wb') as file:
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break
            file.write(data)
    print("File received successful")
    


def check_valid_files(lname, fname):
    full_path = os.path.join(lname, fname)
    return os.path.isfile(full_path)

def list_files(directory):
    return os.listdir(directory)

if __name__ == "__main__":
    start_client()