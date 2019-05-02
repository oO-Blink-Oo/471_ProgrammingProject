import socket
import os
import sys
import subprocess

listenPort = sys.argv[1]

listenPort = int(listenPort, 10)

welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcomeSock.bind(('', listenPort))
welcomeSock.listen(1)

print("Waiting for connections...")
clientSock, addr = welcomeSock.accept()

print("Accepted choice connection from client: ", addr)
print("\n")


def recvAll(sock, numBytes):

    recvBuff = ""

    recvBuff = sock.recv(numBytes)

    return recvBuff


while True:

    choice = recvAll(clientSock, 8)
    bput = "put".encode("utf-8")
    bget = "get".encode("utf-8")
    bquit = "quit".encode("utf-8")
    bls = "ls".encode("utf-8")

    if bquit in choice:
        clientSock.close()
        break

    if bget in choice:

        fileName = recvAll(clientSock, 1024)

        print("File name is:", fileName)

        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSock.bind(('', 0))

        ePort = dataSock.getsockname()[1]
        ePort = str(ePort).encode("utf-8")

        clientSock.send(ePort)

        dataSock.listen(1)

        fileSock, addr = dataSock.accept()

        print("Accepted file connection from client: ", addr)
        print("\n")

        file = open(fileName, 'rb')

        fileData = file.read(1024)

        fileSock.send(fileData)
        print("File sent")

        fileSock.close()
        file.close()

    if bput in choice:

        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSock.bind(('', 0))

        ePort = dataSock.getsockname()[1]
        ePort = str(ePort).encode("utf-8")

        clientSock.send(ePort)

        dataSock.listen(1)

        fileSock, addr = dataSock.accept()

        print("Accepted file connection from client: ", addr)
        print("\n")

        fileData = recvAll(fileSock, 1024)

        print("The file data is: ")
        print(fileData)

        file = open("clientsentfile.txt", 'wb')
        file.write(fileData)

        fileSock.close()
        file.close()

    if bls in choice:

        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSock.bind(('', 0))

        ePort = dataSock.getsockname()[1]
        ePort = str(ePort).encode("utf-8")

        clientSock.send(ePort)

        dataSock.listen(1)

        fileSock, addr = dataSock.accept()

        print("Accepted file connection from client: ", addr)
        print("\n")

        #bList = os.listdir()
        bList = str(os.listdir())
        byteList = bList.encode("utf-8")
        fileSock.send(byteList)

        fileSock.close()
