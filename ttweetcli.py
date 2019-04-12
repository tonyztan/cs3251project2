#!/usr/bin/env python2

"""
Client for Project 2
"""

import socket
import sys

__author__ = 'Matthew Wang and Tony Tan'
__copyright__ = "Copyright 2019, Matthew Wang and Tony Tan"
__license__ = "MIT"
__version__ = "1.0"

def argCheck():
    # Parse and verify command line arguments
    if (len(sys.argv) != 4):
        usage()
    else:
        # Verify IP
        IP = str(sys.argv[1])
        if '.' in IP:
            socket.inet_pton(socket.AF_INET, IP)
        elif ':' in IP:
            socket.inet_pton(socket.AF_INET6, IP)
        else:
            usage()

        # Verify port number
        port = int(sys.argv[2])
        if port < 0 or port > 65535:
            usage()
            
        # return arguments as tuple
        return (sys.argv[1], sys.argv[2], sys.argv[3])

def usage():
    """
    Prints out usage information for the progam and then exits.
    """
    print('Error. Usage:')
    print('To start the client and connect to the server, use the following command and format:')
    print('./ttweetcli.py <ServerIP> <ServerPort> <Username>')
    print('')
    print('ServerIP and ServerPort must be valid.')
    exit()

def runClient(serverHost, serverPort, username):
    # Stores the client's received tweets.
    messages = []

    # Connects to server.
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverHost, int(serverPort)))

    # Sends the server the user's username.
    clientSocket.send("set username " + username)

    exiting = False
    while not exiting:
        response = clientSocket.recv(1024)

        # Server tells client it's ready for a command.
        if (response == "command"):
            command = raw_input("Command: ")

            # Carries out command locally if the command is "timeline".
            if (command == "timeline"):
                for message in messages:
                    print(username + " receive message from " + message)
            messages = []
            # Sends command to server.
            clientSocket.send(command)
        
        # Server sends tweet message to client.
        elif (len(response) > 6 and response[:6] == "tweet "):
            messages.append(response[6:])
        
        # Server tells client to close.
        elif (response == "exit"):
            exiting = True
            print("Goodbye!")

        # Prints a message from the server.
        else:
            print(response)




if __name__ == "__main__":
    """
    Interprets and responds to the command line arguments.
    """
    try:
        serverHost, serverPort, username = argCheck()
        runClient(serverHost, serverPort, username)

    # Ensure that any exceptions lead to a graceful exit with usage information
    except Exception:
        usage()
