# Work by: Alec Trent (ajtrent)
# Sources utilized: https://huskycast.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=070f8e40-f647-479e-852a-ae2900e41682 (Python UDP)

from socket import *

# create a socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

previousSeqNum = 0

# inf loop to cont take input
while True:
    # formatting
    print("")

    # accepts user input, one for each field
    sequenceNumber = input("Enter the Sequence Number: ")
    sequenceNumber = sequenceNumber.rjust(9, '0')# pad out the value if < 9 digits

    typeField = input("Enter the Type: ")
    typeField = typeField.upper()                # uppercase input

    digitsField = input("Enter the Digits: ")
    digitsField = digitsField.rjust(3, '0')      # pad out the value if < 3 digits

    amountField = input("Enter the Amount: ")   
    amountField = amountField.replace('.', '')   # removes decimal point 

    # except the checksum       
    checksum = int(sequenceNumber) + int(amountField)
    checksum = str(checksum).rjust(9, '0')

    # create a packet, convert values to strings
    f1 = str(sequenceNumber)
    f2 = str(typeField)
    f3 = str(digitsField)
    f4 = str(amountField)
    f5 = str(checksum)

    packet = f1 + f2 + f3 + f4 + f5
    print("The packet leaving: ",packet)

    # converts message to bytes, destination, port
    clientSocket.sendto(packet.encode(), ('localhost', 9876))


    # blocks until incoming data arrives for it, holds error/pass value
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    error = modifiedMessage.decode()

    # error handling, checks from server
    if (error == 'a'):
        # do nothing, keeps it from hanging
        passed = 0 
    elif (error == 'b'):
        print("ERROR: Sequence number cannot be less than previously use sequence number")
    elif (error == 'c'):
        print("ERROR: Checksum values do no match!")
    elif (error == 'd'):
        print("ERROR: Sequence number is not 000000000")
    elif (error == 'e'):
        print("ERROR: A valid type was not given, try DEP, WTH, BAL")
    elif (error == 'f'):
        print("ERROR: Digit field is not 000")
    elif (error == 'g'):
        print("ERROR: Amount field is not 0")
    elif (error == 'h'):
        print("ERROR: Checksum is not 000000000")
    else:
        pkt = error
        if (typeField == "BAL"):
            # blocks until incoming data arrives for it
            #modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            #pkt = modifiedMessage.decode()

            # parse it again, use slice to get break the string apart
            #sqNum = pkt[:9]        # dont need this part
            #typ = pkt[9:12]
            digit = pkt[12:15]
            digitV = digit.lstrip('0')  # removes only leading 0s to get true value
            val = 15 + int(digitV)      # might need to add a,  + 1
            amnt = pkt[15:val]
        
            for char in amnt:           # get the last int in the string
                end = char

            if (end == '0'):
                amnt = float(amnt) / 10.00
            else:
                amnt = float(amnt) / 100.00    
    
        print("Current balance: ", amnt)

        
