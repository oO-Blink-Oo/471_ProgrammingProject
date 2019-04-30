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
		continue

	if "put" in choice:

		fileName = choice[4:]
		
		file = open(fileName, "rb")

		fileData = file.read(1024)

		connSock.send(fileData)

		print ("File sent")
	
		file.close()

	if choice == "ls":
		continue


connSock.close()


