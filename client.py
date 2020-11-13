# Lab-1 - Building simple web server
# Name: Khushboo Nilesh Patel
# UTA_ID: 1001863935
# File name: client.py
# python version: 3.8.3

# Import the modules needed to run the script
import socket

# Create a socket object with TCP connection
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port_no = int(input("Enter port number:  "))          # taking port from user
print("Port:  ",port_no)
print('Ready to serve...  ')
servername = input("Enter the ip address:  ")         # taking server from user                         
print("Servername:  ",servername)
filename = input("Enter a filename:  ")              # taking file name from user
print("Filename:  ", filename)    

soc.connect((servername, port_no))                 # Making connection with server
print("\nConnected to Server  \n")               
header = {                                         # Sample header sent to server 
        "Request": "GET /%s HTTP/1.0" % filename,             
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-us",
        "Host": port_no,
    }

http_header = "\r\n".join("%s:%s" % (item, header[item]) for item in header)

print(http_header)                                  # Print the HTTP header response
soc.sendall(http_header.encode())                              
        
while True:                                         # Initiate a process to receive the data           
	data = soc.recv(1024)                           # Read 1024 bytes of data and store it in 'data' variable                                     
	if not data:                                    # If data not present, end printing it
		break
	print(data.decode())                            # Printing data received from server
print("\nSuccessfully received file ")
soc.close()                                         # close the socket
print('\nconnection is closed')