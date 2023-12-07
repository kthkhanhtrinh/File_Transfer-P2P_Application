def authenticate_client(username, password):
    # Receive username and password separately

    
    # For debugging, print the received credentials
    # print(f"Received username: {username}, password: {password}")

    users_file = open("users.txt", "r")
    check = checkExitedAccount(username, password, users_file)
    users_file.close()
    # Check credentials
    if check:
        # client_socket.send("OK".encode("utf-8"))
        print("True")
        # return True
    
    else: print("False")
    # client_socket.send("FAILED".encode("utf-8"))
    # return False 

def register_user(username, password):
    users_file_path = "users.txt"
    try:
        # Check if the username already exists
        with open(users_file_path, "r") as users_file:
            if checkExitedAccount(username, password, users_file):
                print("Account already exists, please choose another name")
                return "Registration failed."

        # If the username is not taken, add the new user
        with open(users_file_path, "a") as users_file:
            users_file.write(f"{username}:{password}\n")

        return "Registration successful. You can now log in."
    except Exception as e:
        return f"Error during registration: {str(e)}"

def checkExitedAccount(username, password, users_file):
    credentials = [line.strip().split(':') for line in users_file]
    
    for stored_username, stored_password in credentials:
        print(stored_username, stored_password)
        if username == stored_username and password == stored_password:
            return True

    return False

username = input("Enter username: ")
password = input("Enter password: ")

result = register_user(username, password)
print(result)
