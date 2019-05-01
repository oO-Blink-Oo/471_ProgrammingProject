import socket
import os
import sys
   
serverAddr = sys.argv[1]
serverPort = sys.argv[2]

serverPort = int(serverPort, 10)
 
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connSock.connect((serverAddr, serverPort))

while True:

	choice = input("ftp> ")

	if choice == "quit":
		break

	if "get" in choice:

		fileName = choice[4:]

		connSock.send(fileName)

		continue

	if "put" in choice:

		bChoice = choice[0:3].encode("utf-8")
		
		connSock.send(bChoice)

		print ("Choice sent")

		ePort = connSock.recv(32)
		ePort = int(ePort, 10)

		fileSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		fileSock.connect((serverAddr, ePort))

		fileName = choice[4:]
		
		file = open(fileName, "rb")

		fileData = file.read(1024)
		
		fileSock.send(fileData)

		print ("File sent")
	
		file.close()

	if choice == "ls":
		continue


fileSock.close()
connSock.close()


