import socket
import sys

listenPort = sys.argv[1]

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
	
    print ("Accepted connection from client: ", addr)
    print ("\n")
	
	# Get the file data
    fileData = recvAll(clientSock, 1024)
	
    print ("The file data is: ")
    print (fileData)

    file = open("sentfile.txt", 'wb')
    file.write(fileData)
		
	# Close our side
    clientSock.close()
    file.close()
	