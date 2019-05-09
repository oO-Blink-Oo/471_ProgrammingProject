Joshua Gomberg
jgomberg@csu.fullerton.edu

Name
Email

Name
Email

Language: Python

How to execute: Run the server file as: python serv.py <PORT NUMBER>
                Run the client file as: cli <server machine> <server port>
                Client commands: ftp> get <file name> (downloads file <file name> from the server)
                                ftp> put <filename> (uploads file <file name> to the server)
                                ftp> ls (lists files on the server)
                                ftp> quit (disconnects from the server and exits)
  
Protocol Design: 
  What kinds of messages will be exchanged across the control channel?
	  Get - Recieves file from server
	  Put - Sends file to server
	  ls	- Displays files on server
	  quit- Terminates connection and turns off the server
    Capable of sending and receiving other messages but they will be rejected with client being told so.

  How should the other side respond to the messages?
	  Get - Server will receive command and file name.  It proceeds to 
		  fetch file.  Initially send file size and then the file itself. Client
		  then recieves size and uses it to prepare for recieving the file. 
      The server will send the file in 2^16 byte chunks 
      and the client will receive the chunks until the file size has been reached.
	  Put - Client send file Name and file size.  It then sends both to the server
		  which uses it to name the file and the size to prepare to recieve the 
		  file. The client will send the file in 2^16 byte chunks 
      and the server will receive the chunks until the file size has been reached.
	  ls	- The server will receive the command and get a list of the files in its directory.
       It will then send the list to the client which will display it.
    quit - Client sends command to server to end connection.
  
  What sizes/formats will the messages have?
	  Sizes- 2^16 bytes max data message size
	  Formats- utf-8
	
  What message exchanges have to take place in order to setup a file transfer channel?
    The file name, size and command.

  How will the receiving side know when to start/stop receiving the file?
    The file size is sent before the data is sent so the client/server knows when the whole file has been sent/received.
  
  How to avoid overflowing TCP buffers?
    The data size sent is limited to 2^16 bytes in each packet.
