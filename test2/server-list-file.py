import socket
import os
import pickle

connected_clients = []

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")
    client_info = {} 
    while True:
        client_socket, addr = server_socket.accept()
        client_address, client_port = addr
        print(f"Connection from {addr}")
        client_info[client_address] = client_address

        connected_clients.append((client_socket, client_address))


        server_command, hostname = input("Server command: ").split()
        
        if hostname != client_address:
            print("Wrong hostname\n")
            return

        if server_command == "discover":
            # client_socket.send("discover".encode())
            handle_server_discover()
        
        if server_command == "ping":
            handle_server_ping(client_socket, client_address)
            break

        if server_command == "quit":
            break

        files_data = client_socket.recv(1024)
        files = pickle.loads(files_data)

        print("List of files in the directory:")

        for file in files:
            print(file)

        #handle publish files

        client_command = client_socket.recv(1024).decode("utf-8").strip()

        if client_command == "publish":
            handle_client_publish(client_socket, client_address)
            server_listening(client_socket, client_address)


        if client_command == "fetch":
            handle_client_fetch(client_socket) 

        client_socket.close()

def handle_client_publish(client_socket, hostname):
    try:
        lname = client_socket.recv(1024).decode("utf-8").strip()
        fname = client_socket.recv(1024).decode("utf-8").strip()
        file_path = os.path.join("..", "public", f"{hostname}_user_published.txt")
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
    pass

def server_listening(client_socket, client_address):
    server_command, hostname = input("Server command: ").split()

    if hostname != client_address:
        return

    if server_command == "discover":
        # client_socket.send("discover".encode())
        handle_server_discover()
    

if __name__ == "__main__":
    main()
