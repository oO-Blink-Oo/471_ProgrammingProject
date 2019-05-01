import socket
import sys

listenPort = sys.argv[1]

listenPort = int(listenPort, 10)

welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcomeSock.bind(('', listenPort))
welcomeSock.listen(1)

def recvAll(sock, numBytes):

	recvBuff = ""
		
	recvBuff = sock.recv(numBytes)
	
	return recvBuff

while True:	

    print ("Waiting for connections...")
		
    clientSock, addr = welcomeSock.accept()
	
    print ("Accepted choice connection from client: ", addr)
    print ("\n")
	
    choice = recvAll(clientSock, 8)
    bput = "put".encode("utf-8")

    if bput in choice:

        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSock.bind(('', 0))
        
        ePort = dataSock.getsockname()[1]
        ePort = str(ePort).encode("utf-8")

        clientSock.send(ePort)
          
        dataSock.listen(1)

        fileSock, addr = dataSock.accept()
        print ("socket accept\n")

        print ("Accepted file connection from client: ", addr)
        print ("\n")

        fileData = recvAll(fileSock, 1024)
	
        print ("The file data is: ")
        print (fileData)

        file = open("sentfile.txt", 'wb')
        file.write(fileData)
		
        fileSock.close()
        clientSock.close()
        file.close()
	