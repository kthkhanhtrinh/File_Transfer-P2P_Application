import socket
import threading

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '0.0.0.0'
    server_port = 12345
    client_sockets = []

    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_host}:{server_port}")

    while True:
        try: 
            client_socket, client_address = server_socket.accept()
            
            print(f"Connection from {client_address}")
            client_sockets.append(client_socket)

            option = client_socket.recv(1024).decode("utf-8").strip()
            print(option.upper())
            
            if option == "login":
                if authenticate_client(client_socket):
                    handle_client(client_socket)
                else:
                    print("Authentication failed. Closing connection.")
                    # client_socket.close()
            elif option == "register":
                user_register(client_socket)

            # Start a new thread to hanent
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except KeyboardInterrupt:
            handle_server_exit(server_socket, client_sockets)

def user_register(client_socket):
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
    print(f"Received username: {username}, password: {password}")

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

def handle_client(client_socket):
    # Implement your file transfer logic here
    receive_file(client_socket)

    client_socket.close()

def receive_file(client_socket):
    with open('received_file.txt', 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            print("File received successfully")
            client_socket.close()
    

def handle_server_exit(server_socket, client_sockets):
    print("Server is exiting. Closing all connections...")
    for client_socket in client_sockets:
        client_socket.close()
    server_socket.close()
    exit()


if __name__ == "__main__":
    start_server()