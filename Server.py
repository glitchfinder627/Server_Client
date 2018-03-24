import time
import threading
import socketserver

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

    HOST, PORT = "localhost", 8745

    with ThreadedTCPServer((HOST, PORT), TCPRequestHandler) as server:

        print("Server address - {}:{}".format(server.server_address[0],str(server.server_address[1])))

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)

        while True:
            time.sleep(50)

        server.shutdown()
