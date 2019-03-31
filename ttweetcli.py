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

def usage():
    # TODO: Update Usage Information
    """
    Prints out usage information for the progam and then exits.
    """

    print 'Error. Usage:'
    print 'To upload: ./ttweetcli.py -u <ServerIP> <ServerPort> "<Message>"'
    print 'To download: ./ttweetcli.py -d <ServerIP> <ServerPort>'
    print 'ServerIP and ServerPort must be valid.'
    print 'Message must be 150 or less characters.'
    exit()



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

        #TODO: Add Implementation Here

        else:
            usage()

    # Ensure that any exceptions lead to a graceful exit with usage information
    except Exception:
        usage()


main()
