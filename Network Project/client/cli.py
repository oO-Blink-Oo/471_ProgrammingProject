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

        bChoice = choice[0:4].encode("utf-8")
        connSock.send(bChoice)

        connSock.close()
        break

    if "get" in choice:

        bChoice = choice[0:3].encode("utf-8")
        connSock.send(bChoice)

        print("Choice sent")

        fileName = choice[4:]
        fileName = fileName.encode("utf-8")
        connSock.send(fileName)

        print("File name sent")

        ePort = connSock.recv(32)
        ePort = int(ePort, 10)

        fileSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fileSock.connect((serverAddr, ePort))

        fileData = fileSock.recv(1024)
        print("The file data is: ")
        print(fileData)

        file = open("serversentfile.txt", 'wb')
        file.write(fileData)

        file.close()
        fileSock.close()

    if "put" in choice:

        bChoice = choice[0:3].encode("utf-8")
        connSock.send(bChoice)

        print("Choice sent")

        ePort = connSock.recv(32)
        ePort = int(ePort, 10)

        fileSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fileSock.connect((serverAddr, ePort))

        fileName = choice[4:]

        file = open(fileName, "rb")
        fileData = file.read(1024)

        fileSock.send(fileData)
        print("File sent")

        file.close()
        fileSock.close()

    if choice == "ls":

        bChoice = choice[0:2].encode("utf-8")
        connSock.send(bChoice)

        print("Choice sent")
