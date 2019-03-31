#!/usr/bin/env python2

"""
Client for Trivial Twitter application (or ttweet).
In this application a ttweet server has room for exactly one message and is used by exactly one client.
The client uploads a message to the server, then the same or another client downloads the message to read it.
An uploaded message is stored at the server will overwrite an existing message if the server already has a message.
A download request returns the last uploaded message or returns 'Empty Message' if no message has been uploaded yet.
The server is simple and can handle only one client at a time.
"""

import socket
import sys

__author__ = 'Tony Z. Tan'
__copyright__ = "Copyright 2019, Tony Z. Tan"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "tonytan@gatech.edu"

def usage():
    """
    Prints out usage information for the progam and then exits.
    """

    print 'Error. Usage:'
    print 'To upload: ./ttweetcli.py -u <ServerIP> <ServerPort> "<Message>"'
    print 'To download: ./ttweetcli.py -d <ServerIP> <ServerPort>'
    print 'ServerIP and ServerPort must be valid.'
    print 'Message must be 150 or less characters.'
    exit()

def upload(IP, port, message):
    """
    Uploads the specified message to the server at the specified IP and port.
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, port))
    client_socket.send("upload=" + message)
    client_socket.close()

def download(IP, port):
    """
    Downloads the message stored at the server at the specified IP and port.
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, port))
    client_socket.send("download=")
    buf = client_socket.recv(256)
    if len(buf) > 0:
        client_socket.close()
        return buf

def main():
    """
    Interprets and responds to the command line arguments.
    """

    if len(sys.argv) != 4 and len(sys.argv) != 5:
        usage()

    try:
        mode = str(sys.argv[1])

        # Verify that the IP is valid
        IP = str(sys.argv[2])
        if '.' in IP:
            socket.inet_pton(socket.AF_INET, IP)
        elif ':' in IP:
            socket.inet_pton(socket.AF_INET6, IP)
        else:
            usage()

        # Verify that the port number is valid
        port = int(sys.argv[3])
        if port < 0 or port > 65535:
            usage()

        # If -u argument is invoked with correct parameters, upload message
        if mode == "-u" and len(sys.argv) == 5:
            message = str(sys.argv[4])
            if len(message) > 150:
                usage()
            upload(IP, port, message)
            server_message = download(IP, port)
            if (server_message == message or (server_message == "Empty Message" and message == "")):
                print "Message upload successful"
            exit()

        # If -d argument is invoked with correct parameters, download message
        elif mode == "-d" and len(sys.argv) == 4:
            server_message = download(IP, port)
            print server_message
            exit()

        else:
            usage()

    # Ensure that any exceptions lead to a graceful exit with usage information
    except Exception:
        usage()


main()
