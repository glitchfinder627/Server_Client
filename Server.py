import time
import threading
import socketserver
import os

class TCPRequestHandler(socketserver.BaseRequestHandler):
	def handle(self):
		while True:
			try:
				data = self.request.recv(1024)
				if data:
					cur_thread = threading.current_thread()
					print("\nServer Received: {}".format(data.decode()))
					sresponse = "{}: {}".format(cur_thread.name, data.decode())
					response = bytes("{}: {}".format(cur_thread.name, data.decode()), 'ascii')
					print("\nServer Sent : {}".format(sresponse))
					self.request.sendall(response)
			except:
				print("Connection with the client lost")
				self.close_connection = True
				break

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
	
	ON_HEROKU = os.environ.get('ON_HEROKU')

	port = None
	if ON_HEROKU:
	    # get the heroku port
	    port = int(os.environ.get('PORT', 8745))  # as per OP comments default is 17995
	else:
	    port = 8745	
	
	print(port)	

	HOST, PORT = "localhost", port

	server = ThreadedTCPServer((HOST, PORT), TCPRequestHandler)
	print("Server address - {}:{}".format(server.server_address[0],str(server.server_address[1])))
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	print("Server loop running in thread:", server_thread.name)

	while True:
		time.sleep(50)

	server.shutdown()
