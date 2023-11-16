import socket
import threading


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

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    
    connected = True
    while connected:
        option = conn.recv(1024).decode("utf-8").strip()
        print(option.upper())
        
        if option == "login":
            if authenticate_client(conn):
                receive_file(conn)
            else:
                print("Authentication failed. Closing connection.")
                conn.close()
        elif option == "register":
            user_register(conn)
            conn.close()
            connected = False

    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '0.0.0.0'
    server_port = 12345
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_host}:{server_port}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()