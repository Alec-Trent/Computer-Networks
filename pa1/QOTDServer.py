# Work by: Alec Trent (ajtrent)
# Sources utilized: https://huskycast.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=070f8e40-f647-479e-852a-ae2900e41682 (Python UDP)

from socket import *
import random

# create a socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
print("Socket is created")

# bind the socket to a port
serverSocket.bind(('', 9876))
print("Socket bound to port 9876, server is ready to receive")

# inf loop to cont take input
while True:
    # formatting
    print("")

    message, clientAddress = serverSocket.recvfrom(2048)
    print("Data received")

    # get string version of message passed
    modifiedMessage = message.decode()
    print("Decoded the message ", modifiedMessage)

    # check to make sure correct packet text passed
    if modifiedMessage != 'qotd':
        print("ERROR: The proper input is keystroke q. The check on text qotd has failed")
    else:
        print("Performed a check on the modified message")

        # return a number in the range(start (included), stop (not included), step)
        quoteNumber = random.randrange(1, 11, 1)
        print("QuoteNumber generated: ", quoteNumber)

        # based on generated number choose a quote
        if quoteNumber == 1:
            quote = "Nothing is impossible, the word itself says 'I'm possible'! - Audrey Hepburn"
        elif quoteNumber == 2:
            quote = "Don't judge each day by the harvest you reap but by the seeds that you plant. - Robert Louis Stevenson"
        elif quoteNumber == 3:
            quote = "Perfection is not attainable, but if we chase perfection we can catch excellence. - Vince Lombardi"
        elif quoteNumber == 4:
            quote = "Start by doing what's necessary; then do what's possible; and suddenly you are doing the impossible. - Francis of Assisi"
        elif quoteNumber == 5:
            quote = "Keep your face always toward the sunshine - and shadows will fall behind you. - Walt Whitman"
        elif quoteNumber == 6:
            quote = "Do your little bit of good where you are; it's those little bits of good put together that overwhelm the world. - Desmond Tutu"
        elif quoteNumber == 7:
             quote = "The best preparation for tomorrow is doing your best today. - H. Jackson Brown, Jr."
        elif quoteNumber == 8:
            quote = "Put your heart, mind, and soul into even your smallest acts. This is the secret of success. - Swami Sivananda"
        elif quoteNumber == 9:
            quote = "I can't change the direction of the wind, but I can adjust my sails to always reach my destination. - Jimmy Dean"
        elif quoteNumber == 10:
            quote = "The best and most beautiful things in the world cannot be seen or even touched - they must be felt with the heart. - Helen Keller"
        else:
            quote = "Error: Not a valid quote number"

        print("Sending requested quote")
        serverSocket.sendto(quote.encode(), clientAddress)

