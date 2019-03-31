#!/usr/bin/env python2

"""
Server for Project 2.
"""

import socket
import sys

__author__ = 'Matthew Wang and Tony Tan'
__copyright__ = "Copyright 2019, Matthew Wang and Tony Tan"
__license__ = "MIT"
__version__ = "1.0"

def usage():
    """
    Prints out usage information for the progam and then exits.
    """

    print 'Error. Usage: ./ttweetsrv.py <ServerPort>'
    print 'ServerPort must be valid.'
    exit()

def server(port):
    # TODO: Implement Server
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
                pass
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
