#!/usr/bin/env python2

"""
Server for Trivial Twitter application (or ttweet).
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

    print 'Error. Usage: ./ttweetsrv.py <ServerPort>'
    print 'ServerPort must be valid.'
    exit()

def server(port):
    """
    Runs the server at the specified port.
    """

    try:
        stored_message = ""
        empty_message = "Empty Message"

        # Create the server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.listen(1)

        print "Server is running. Ctrl + C to quit."

        while True:
            try:
                # Accept connections and receive data
                connection, address = server_socket.accept()
                buf = connection.recv(256)
                if len(buf) > 0:
                    try:
                        # Interpret and respond to received data
                        new_message = str(buf)
                        if len(new_message) > 0 and len(new_message) < 158:
                            if new_message[0:7] == "upload=":
                                stored_message = new_message[7:]
                            elif new_message[0:9] == "download=":
                                if len(stored_message) == 0:
                                    connection.send(empty_message)
                                else:
                                    connection.send(stored_message)
                    except ValueError:
                        pass
                    connection.close()
            # Ensure that any exception does not shut down the server
            except Exception:
                pass

    except KeyboardInterrupt:
        exit()

    # Ensure that any exceptions lead to a graceful exit with usage information
    except:
        usage()

def main():
    """
    Interprets and responds to the command line arguments.
    """

    if len(sys.argv) != 2:
        usage()

    try:
        port = int(sys.argv[1])
    except ValueError:
        usage()

    if port < 0 or port > 65535:
        usage()

    server(port)

main()
