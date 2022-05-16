# Work by: Alec Trent (ajtrent)
# Sources utilized: https://huskycast.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=070f8e40-f647-479e-852a-ae2900e41682 (Python UDP)

from socket import *

# create a socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
print("Socket is created")

# bind the socket to a port
serverSocket.bind(('', 9876))
print("Socket bound to port 9876, server is ready to receive")

initialBalance = 23540.00
print("Your initial balance is ", initialBalance)

prevSqNum = 0   # keep track of largest sequence number

# inf loop to cont take input
while True:
    # formatting
    print("")

    message, clientAddress = serverSocket.recvfrom(2048)
    print("Data received")

    # when it gets packet, print it
    # get string version of packet passed
    packet = message.decode()
    print("Decoded the packet ", packet)

    # use slice to get break the string apart
    sqNum = packet[:9]  
    typ = packet[9:12]
    digit = packet[12:15]
    if (digit != '000'):
        digitVal = digit.lstrip('0')    # removes only leading 0s to get true value
        val = 15 + int(digitVal)
        amnt = packet[15:val]
        chksum = packet[val:val + 9]
    else:
        amnt = packet[15:16]
        chksum = packet[16:25]

    # chatty 
    print("Sequence Number: ", sqNum)
    print("Type Field: ", typ)
    print("Digit Field: ", digit)
    print("Amount Field: ", amnt)
    print("Checksum Field: ", chksum)


    # calculate checksum again to make sure the values are correct
    ckSum = int(sqNum) + int(amnt)
    ckSum = str(ckSum).rjust(9, '0')


    # do not send a packet back
    if (typ == "DEP" or typ == "WTH"):

        # make sure sequence number is strictly increasing
        if (int(sqNum) <= int(prevSqNum)):
            print("ERROR: Sequence number cannot be less than previously use sequence number")
            err = 'b'
            serverSocket.sendto(err.encode(), clientAddress)

        elif (chksum != ckSum):
            print("ERROR: Checksum values do no match!")
            err = 'c'
            serverSocket.sendto(err.encode(), clientAddress)

        else:
            prevSqNum = sqNum   # update the max sequence number

            print("Checksum validation PASSED")

            ant = float(int(amnt) / 100)

            if(typ == "DEP"):   
                print("Value to be deposited: ", ant)
                initialBalance = initialBalance + ant     # add money to balance
                print("New balance: ", initialBalance)
            else:
                print("Value to be withdrawn: ", ant)
                initialBalance = initialBalance - ant     # remove money from balance
                print("New balance: ", initialBalance)

            # we passed with no error, stops the wait from blocking
            err = 'a'
            serverSocket.sendto(err.encode(), clientAddress)

    # send back a packet
    elif (typ == "BAL"):

        # make sure sequence number matches the 9x 0's
        if (sqNum != '000000000'):
            print("ERROR: Sequence number is not 000000000")
            err = 'd'
            serverSocket.sendto(err.encode(), clientAddress)

        elif(digit != '000'):
            print("ERROR: Digit field is not 000")
            err = 'f'
            serverSocket.sendto(err.encode(), clientAddress)

        elif(amnt != '0'):
            print("ERROR: Amount field is not 0")
            err = 'g'
            serverSocket.sendto(err.encode(), clientAddress)

        elif(chksum != ckSum):
            print("ERROR: Checksum is not 000000000")
            err = 'h'
            serverSocket.sendto(err.encode(), clientAddress)

        else:
            prevSqNum = str(prevSqNum).rjust(9, '0')    # padding

            bal = str(initialBalance).replace('.', '')  # remove the period

            leng = len(bal)
            leng = str(leng).rjust(3,'0')               # padding

            cSum = int(prevSqNum) + int(bal)
            cSum = str(cSum).rjust(9, '0')              # padding

            f1 = str(prevSqNum)
            f2 = str(typ)
            f3 = str(leng)              # length of initBalance
            f4 = str(bal)               # current balance as amount
            f5 = str(cSum)

            pcket = f1 + f2 + f3 + f4 + f5
            print("Balance request packet: ", pcket)
            print("Current Balance: ", initialBalance)

            serverSocket.sendto(pcket.encode(), clientAddress)

    else:
        print("ERROR: A valid type was not given, try DEP, WTH, BAL")
        err = 'e'
        serverSocket.sendto(err.encode(), clientAddress)

