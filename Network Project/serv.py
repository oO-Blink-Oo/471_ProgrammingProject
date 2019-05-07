import socket
import os
import sys

# Get the command line argument
listenPort = sys.argv[1]
listenPort = int(listenPort, 10)

# Set up the connection socket
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcomeSock.bind(('', listenPort))

# Listen and accept the connection
welcomeSock.listen(1)
print("Waiting for connections...")
clientSock, addr = welcomeSock.accept()
print("Accepted control connection from client: ", addr)
print("\n")

# Function to receive all data sent


def recvAll(sock, numBytes):

    # Initialize buffers
    recvBuff = ""
    tmpBuff = ""

    # Loop until the buffer is greater than number of bytes total
    while len(recvBuff) < numBytes:

        # Receive 65536 bytes of data
        tmpBuff = sock.recv(65536)

        # Check if all the data has been sent
        if not tmpBuff:
            break

        # Append the data to itself
        recvBuff += tmpBuff.decode("utf-8")

    # Return the data
    return recvBuff


# Keep accepting commands
while True:

    # Receive the choice
    choice = clientSock.recv(8)

    # Encoded commands for comparison
    bput = "put".encode("utf-8")
    bget = "get".encode("utf-8")
    bquit = "quit".encode("utf-8")
    bls = "ls".encode("utf-8")

    # Quit command
    if bquit in choice:

        # Close the client socket, stop accepting commands and print success message
        clientSock.close()
        print("Quit success\n")
        break

    # Get command
    elif bget in choice:

        # Receive the file name
        fileName = clientSock.recv(1024)

        try:
            # Open the file and read it
            file = open(fileName, 'rb')
            fileData = file.read()

            # Send the file size to the server
            fileSize = len(fileData)
            clientSock.send(str(fileSize).encode("utf-8"))

            # Create the ephemeral port and send the port number to the client
            dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataSock.bind(('', 0))
            ePort = dataSock.getsockname()[1]
            ePort = str(ePort).encode("utf-8")
            clientSock.send(ePort)

            # Listen and accept the connection
            dataSock.listen(1)
            fileSock, addr = dataSock.accept()

            # Initialize number of bytes sent
            numSent = 0

            # Loop over the whole file size
            while numSent < fileSize:

                # Send 65536 bytes of data at a time
                fileBuf = fileData[numSent:numSent+65536]
                fileSock.send(fileBuf)
                numSent += 65536

            # Close the file and data socket and print success message
            fileSock.close()
            file.close()
            print("Get success\n")
        except FileNotFoundError:
	        print("File Not Found")

    # Put command
    elif bput in choice:

        # Receive the file name
        fileName = clientSock.recv(1024)

        # Receive the file size
        fileSize = clientSock.recv(1024)

        # Create the ephemeral port and send the port number to the client
        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSock.bind(('', 0))
        ePort = dataSock.getsockname()[1]
        ePort = str(ePort).encode("utf-8")
        clientSock.send(ePort)

        # Listen and accept the connection
        dataSock.listen(1)
        fileSock, addr = dataSock.accept()

        # Get all the file data
        fileData = recvAll(fileSock, int(fileSize))

        # Open the file and write the data to it
        file = open(fileName, "wb")
        file.write(fileData.encode("utf-8"))

        # Close the file and data socket and print success message
        fileSock.close()
        file.close()
        print("Put success\n")

    # ls command
    elif bls in choice:

        # Create the ephemeral port and send the port number to the client
        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSock.bind(('', 0))
        ePort = dataSock.getsockname()[1]
        ePort = str(ePort).encode("utf-8")
        clientSock.send(ePort)

        # Listen and accept the connection
        dataSock.listen(1)
        fileSock, addr = dataSock.accept()

        # Get the file list and send it to the client
        bList = str(os.listdir())
        byteList = bList.encode("utf-8")
        fileSock.send(byteList)

        # Close the data socket and print success message
        fileSock.close()
        print("ls success\n")
    else:
	    print("Command not identified")
