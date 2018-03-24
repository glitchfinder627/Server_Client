import socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print("Failed to connect")
	sys.exit();

print("Socket Created")

host = "localhost"
port = 8745

print("IP Address - {}:{} ".format(host,port))

s.connect((host,port))

print("Socket Connected using IP: " + host)

while True:
	message = input("Enter message: ")
	try:
		s.sendall(message.encode())
	except socket.error:
		print("Did not send successfully")
		sys.exit();
	print("Message sent successfully")
	print("Client sent: " + message)
	reply = s.recv(4096)
	print("Client received: " + reply.decode())

s.close()
