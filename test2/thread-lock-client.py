# Import socket module
import socket


def Main():
	host = '127.0.0.1'

	port = 12345
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	s.connect((host,port))

	# message you send to server
	message = "shaurya says geeksforgeeks"
	while True:

		# message sent to server
		s.send(message.encode('ascii'))

		# message received from server
		data = s.recv(1024)

		print('Received from the server :',str(data.decode('ascii')))

		# ask the client whether he wants to continue
		ans = input('\nDo you want to continue(y/n) :')
		if ans == 'y':
			continue
		else:
			break
	# close the connection
	s.close()

if __name__ == '__main__':
	Main()
