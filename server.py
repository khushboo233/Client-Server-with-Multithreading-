# Lab-1 - Building simple web server
# Name: Khushboo Nilesh Patel
# UTA_ID: 1001863935
# File name: server.py
# python version: 3.8.3

# Import the modules needed to run the script
from socket import *
import threading
import argparse
import sys

line_parser = argparse.ArgumentParser(description = "Description for my parser")                        # making an ArgumentParser object
line_parser.add_argument("-port", help = "Example: port number", required = False, default = "54321")   # making calls to the add_argument() method.
argument = line_parser.parse_args()

port_no = int(argument.port)                                    # Reading port number

print("Port:  ",port_no)                                        # Printing port number
print('Ready to serve...  \n')


class ClientThread(threading.Thread):                           # Create a thread class for creating client threads

    def __init__(self,ip,port,sock):                         
        threading.Thread.__init__(self)                         # Intializing the class
        self.ip = ip                                            # Assign ip to self.ip
        self.port = port                                        # Assign port number to self.port
        self.sock = sock                                        # Assign sock to self.sock
        print("\nNew thread is started for "+ip+":"+str(port))  # New thread created 

    def run(self):                                              # Initiate the process to read the msg_client
        try:
            msg_client = self.sock.recv(1024)                   # Get 1024 bytes of msg_client from the client
            print(msg_client)                                   # Print the msg_client 
            if len(msg_client.split()) > 0:                     # Split the msg_client
               print(msg_client.split()[1])                     # filename is stored in msg_client.split()[1] 

            filename = msg_client.split()[1]                    # filename stored in a variable
            f = open(filename[1:])                              # opening client demanded file
            data = f.read()                                     # Reading client demanded file
            f.close()                                           # Closing client demanded file

            header_info = {                                     # Sample header information
            "Content-Length": len(data),
            "Keep-Alive": "timeout=%d,max=%d" % (10, 100),
            "Connection": "Keep-Alive",
            "Content-Type": "text/html"
            }
            header_body = "\r\n".join("%s:%s" % (item, header_info[item]) for item in header_info)

            print(header_body)                                                   # Print the HTTP header response                                                              
            
            self.sock.sendall(b'HTTP/1.0 200 OK\nContent-Type: text/html\n\n')   # Passing HTTP/1.0 200 OK response msg_client and displaying file in command prompt

            self.sock.sendall(b'Thread number: ')
            self.sock.send(str(self.port).encode())
            self.sock.send(b'\n\n')
            self.sock.send(data.encode())                                        # Send the output data to the client socket
            print('\nFile successfully sent \n\n\n\n')                           # When a file is successfully sent

            self.sock.close()                                                    # Close the socket
        except IOError:                                                          # If error occurs, then exception
            self.sock.sendall(b'HTTP/1.0 404 NOT FOUND - File Not Found')        # Response msg_client for "File not found" 
            self.sock.close()                                                    # Close the socket
       

soc = socket(AF_INET, SOCK_STREAM)                                               # Prepare a server socket
threads = [];                                                                    # Creating a variable for storing threads

try:
    soc.bind(('',port_no))                                                       # Bind socket                  
    print("\nsocket binding completed")
    
except socket.error as msg:                                                      # Exception for binding failure
	print('\nBind failed. Error code :' + str(msg[0])+ 'msg_client' + msg[1])
	sys.exit()

soc.listen(10)                                                   # Listening to client
print("\nsocket is listening")

while True:
    print("\nWaiting for new connections... ")
    (conn, (ip,port_no)) = soc.accept()                          # Establish the connection
    print('\nGot connection from ', (ip,port_no))                # Print the ip address and port number of the client
    newthread = ClientThread(ip,port_no,conn)                    # Create a new variable for creating thread
    newthread.start()                                            # Start multi-threading
    threads.append(newthread)                                    # Append new thread

for t in threads:                                                # Add more clients to the thread                                                          
    t.join()                                                                   