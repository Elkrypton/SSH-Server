import store
import socket
import threading
import json
import paramiko
from server import Server

host_keys = paramiko.RSAKey(filename="id_rsa")




class Connection():

	def __init__(self, host, port):


		self.host = host 
		self.port = int(port)

	def create_connection(self):

		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		try:
			sock.bind((self.host,self.port))
		except Exception as e:
			print("[-] Failed : {}".format(str(e)))

		print("++> Listening on {}:{}".format(self.host, self.port))
		sock.listen(100)
		client,addr = sock.accept()
		save = store.Store(addr)
		if addr:

			save.store_ip(addr)




		print("""\t\t\n[+] Got connection from

				HOST : {}
				PORT : {}""".format(addr[0],addr[1]))

		while True:
			#sock.send("\t\t Crypton welcomes you bb")
			t = threading.Thread(target=self.handle_client, args=(client,))
			t.start()
			data = self.receive_data(sock)
			if data:
				save.store_data(data)
				#self.convert(data)
				print(data)
				break
			if not data:
				break


	def handle_client(self,client):


		try:
			bhsession = paramiko.Transport(client)
			bhsession.add_server_key(host_keys)
			server = Server()
			try:
				bhsession.start_server(server=server)
			except SSHException as x:
				print("[-] error : {}".format(str(x)))

			print("authenticated !")
			chand = bhsession.accept(20)
			chand.send("Second welcoming ")
			data = self.receive_data(chand)
			save = store.Store(data)
			print(data)
			while True:

				try:
					command = raw_input("<#>").rstrip("\n")
					if command != "exit":

						chand.send(command)
						data = self.receive_data(chand)
						save.store_data(data)
						#self.convert(data)
						print(data)

					else:
						chand.send('exit')
						print("exiting.......")
						bhsession.close()
						raise Exception('exit')
				except KeyboardInterrupt:
					bhsession.close()
					sys.exit(0)

		except Exception as s:
			print("[-] Something is wrong : {}".format(str(s)))
			chand.send(str(s))



	def receive_data(self,connection):

		buffer = ''
		connection.settimeout(2)
		try:
			data = connection.recv(1024)

			buffer += data 

		except:
			pass
		return buffer


print(
"""
 /$$      /$$            /$$$$$$                                  /$$
| $$$    /$$$           /$$__  $$                                | $$
| $$$$  /$$$$  /$$$$$$ | $$  \__/  /$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$    /$$$$$$  /$$$$$$$
| $$ $$/$$ $$ /$$__  $$| $$       /$$__  $$| $$  | $$ /$$__  $$|_  $$_/   /$$__  $$| $$__  $$
| $$  $$$| $$| $$  \__/| $$      | $$  \__/| $$  | $$| $$  \ $$  | $$    | $$  \ $$| $$  \ $$
| $$\  $ | $$| $$      | $$    $$| $$      | $$  | $$| $$  | $$  | $$ /$$| $$  | $$| $$  | $$
| $$ \/  | $$| $$   /$$|  $$$$$$/| $$      |  $$$$$$$| $$$$$$$/  |  $$$$/|  $$$$$$/| $$  | $$
|__/     |__/|__/  |__/ \______/ |__/       \____  $$| $$____/    \___/   \______/ |__/  |__/
                                            /$$  | $$| $$
                                           |  $$$$$$/| $$
                                            \______/ |__/

          
                   SSH Server Connection v1
                   copyright@ : Rochdi El Majdoub
                   Digital name : Mr.Crypton
"""
)

host = input("[+] Host:")
port = int(input("[+] Port:"))
conn = Connection(host,port)
conn.create_connection()
