# Work by: Alec Trent (ajtrent)
# Sources utilized: https://huskycast.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=070f8e40-f647-479e-852a-ae2900e41682 (Python UDP)

from socket import *

# create a socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# accepts user input
message = input("Press q to get a quote now: ")

# if correct input given, set text message to pass to server
if message == "q":
    message = "qotd"
else:
    print("Error: Incorrect input")
    # release the socket
    clientSocket.close()
    quit()

# converts message to bytes, destination, port
clientSocket.sendto(message.encode(), ('localhost', 9876))

# blocks until incoming data arrives for it
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# display quote
print("Quote of the day: ", modifiedMessage.decode())

# release the socket
clientSocket.close()

