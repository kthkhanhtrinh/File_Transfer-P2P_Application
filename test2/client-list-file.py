import socket
import pickle
import os

def receive_files(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Receive the serialized data
    server_command = client_socket.recv(1024).decode("utf-8").strip()

    if server_command == "discover":
        directory = "..\\public"
        files = list_files(directory)
        files_data = pickle.dumps(files)
        client_socket.send(files_data)

    if server_command == "ping":
        client_socket.send("ping".encode())
        print("Ping request received. Pinging back to the server.")
        client_socket.send("pong".encode())
    
    #client_command :publish lname fname
    client_command = input("Enter command (publish/fetch), lname, fname: ")
    client_command, lname, fname = client_command.split(" ")
    try:
        # if client_command != "publish" or client_command != "fetch":
        #     client_socket.close()
        #     return
        
        client_socket.send(client_command.encode())

        if client_command == "publish":
            handle_client_publish(client_socket, client_command, lname, fname)

        if client_command == "fetch":
            handle_client_fetch(fname)

    except ValueError:
        print("Invalid command format. Expected: publish lname fname")
        client_socket.close()
        return


    # Deserialize the data using pickle

    client_socket.close()

def handle_client_publish(client_socket, client_command, lname, fname):
    if check_valid_files(lname, fname):
        client_socket.send(lname.encode())
        client_socket.send(fname.encode())
    else:
        print("Wrong lname or fname, Please check again")
        

def handle_client_fetch(fname):
    pass


def check_valid_files(lname, fname):
    full_path = os.path.join(lname, fname)
    return os.path.isfile(full_path)

def list_files(directory):
    return os.listdir(directory)

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345
    receive_files(host, port)
