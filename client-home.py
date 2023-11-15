import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '192.168.1.15' #change to your IP addrs
    server_port = 12345

    client_socket.connect((server_host, server_port))

    option = input("Select option (login/register): ")
    client_socket.send(option.encode())

    if (option == "login"):
        if authenticate_client(client_socket):
            send_file(client_socket)
        else:
            print("Authentication failed. Exiting.")
    elif (option == "register"):
        if user_register(client_socket):
            print("Register successfully")
        else:
            print("Register failed. Exiting")
    client_socket.close()

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

if __name__ == "__main__":
    start_client()
