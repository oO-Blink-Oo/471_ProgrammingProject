import socket
import os
import sys

# Get the command line arguments
serverAddr = sys.argv[1]
serverPort = sys.argv[2]
serverPort = int(serverPort, 10)

# Set up the connection socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connSock.connect((serverAddr, serverPort))

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


# Run commands indefinitely
while True:

    # Get the input choice from the user
    choice = input("ftp> ")

    # Quit command
    if choice == "quit":

        # Send choice to server
        bChoice = choice[0:4].encode("utf-8")
        connSock.send(bChoice)

        # Close the connection socket and end the command loop
        connSock.close()
        break

    # Get command
    if "get" in choice:

        # Send choice to server
        bChoice = choice[0:3].encode("utf-8")
        connSock.send(bChoice)

        # Send file name to server
        fileName = choice[4:]
        fileName = fileName.encode("utf-8")
        connSock.send(fileName)
        print("File name: ", fileName.decode("utf-8"))

        # Receive the file size
        fileSize = connSock.recv(1024)
        print("File size: ", fileSize.decode("utf-8"), "bytes\n")

        # Receive ephemeral port number and connect to it
        ePort = connSock.recv(32)
        ePort = int(ePort, 10)
        fileSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fileSock.connect((serverAddr, ePort))

        # Get all the file data
        fileData = recvAll(fileSock, int(fileSize))

        # Open the file and write the data to it
        file = open(fileName, 'wb')
        file.write(fileData.encode("utf-8"))

        # Close the file and data socket
        file.close()
        fileSock.close()

    # Put command
    if "put" in choice:

        # Send choice to server
        bChoice = choice[0:3].encode("utf-8")
        connSock.send(bChoice)

        # Send file name to server
        fileName = choice[4:]
        fileName = fileName.encode("utf-8")
        connSock.send(fileName)
        print("File name: ", fileName.decode("utf-8"))

        # Open the file and read it
        file = open(fileName, "rb")
        fileData = file.read()

        # Send the file size to the server
        fileSize = len(fileData)
        connSock.send(str(fileSize).encode("utf-8"))
        print("File size: ", fileSize, "bytes\n")

        # Receive ephemeral port number and connect to it
        ePort = connSock.recv(32)
        ePort = int(ePort, 10)
        fileSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fileSock.connect((serverAddr, ePort))

        # Initialize number of bytes sent
        numSent = 0

        # Loop over the whole file size
        while numSent < fileSize:

            # Send 65536 bytes of data at a time
            fileBuf = fileData[numSent:numSent+65536]
            fileSock.send(fileBuf)
            numSent += 65536

        # Close the file and data socket
        file.close()
        fileSock.close()

    # ls command
    if choice == "ls":

        # Send choice to server
        bChoice = choice[0:2].encode("utf-8")
        connSock.send(bChoice)

        # Receive ephemeral port number and connect to it
        ePort = connSock.recv(32)
        ePort = int(ePort, 10)
        fileSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fileSock.connect((serverAddr, ePort))

        # Receive the data and print it
        fileData = fileSock.recv(1024)
        print(fileData.decode("utf-8"))
