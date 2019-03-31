#!/usr/bin/env python2

"""
Server for Project 2.
"""

import select
import socket
import sys
import Queue

__author__ = 'Matthew Wang and Tony Tan'
__copyright__ = "Copyright 2019, Matthew Wang and Tony Tan"
__license__ = "MIT"
__version__ = "1.0"

# Placeholder variables to make them accessible to all methods
inputs = []
outputs = []
messsage_queues = {}
connected_users = {}

def usage():
    """
    Prints out usage information for the progam and then exits.
    """

    print 'Error. Usage: ./ttweetsrv.py <ServerPort>'
    print 'ServerPort must be valid.'
    exit()

def send_to_client(connection, data):
    """
    This method is used to send the specified data to the connection socket.
    It works by adding the information to the appropriate queues.
    """
    message_queues[connection].put(data)
    if connection not in outputs:
        outputs.append(connection)

def handle_request(connection, request):
    if (len(request) > 13) and (request[0:13] == "set username "):
        # TODO: username logic goes here

    elif (len(request) > 12) and (request[0:12] == "unsubscribe "):
        # TODO: unsubscribe logic goes here

    elif (len(request) > 10) and (request[0:10] == "subscribe "):
        # TODO: subscribe logic goes here

    elif (len(request) == 9) and (request == "timeline"):
        # TODO: timeline logic goes here

    elif (len(request) > 6) and (request[0:6] == "tweet "):
        # TODO: tweet logic goes here

    elif (len(request) == 4) and (request == "exit"):
        # TODO: exit logic goes here

    else:
        # TODO: invalid request logic goes here

# Consulted: https://pymotw.com/2/select/
def server(port):
    """
    Runs the server at the specified port.
    """

    try:

        # Create the server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setblocking(0)

        server_socket.bind(('', port))
        server_socket.listen(5)

        print "Server is running. Ctrl + C to quit."

        while True:
            try:
                # Sockets to check for incoming data
                inputs = [server_socket]

                # Sockets to use for outgoing data
                outputs = []

                # Dictionary. Key: Connection. Value: Queue for outgoing data.
                messsage_queues = {}

                # Dictionary. Key: Connection. Value: [Username, Subscribed hashtags].
                connected_users = {}

                while inputs:
                    readable, writable, exceptional = select.select(inputs, outputs, inputs)

                    # Handle incoming data
                    for s in readable:
                        # Handle server sockets that are waiting to accept a connection
                        if s is server:
                            connection, client_address = s.accept()
                            connection.setblocking(0)
                            inputs.append(connection)

                            # Create a queue for the accepted connection
                            message_queues[connection] = Queue.Queue()

                        # Handle server sockets that are ready to be read from
                        else:
                            data = s.recv(1024)
                            # If there is data received, handle the data
                            if data:
                                handle_request(s, data)

                            # If there is no data received, close stream
                            else:
                                inputs.remove(s)
                                if s in outputs:
                                    outputs.remove(s)
                                s.close()
                                del message_queues[s]

                    # Handle outgoing data
                    for s in writable:
                        try:
                            next_message = message_queues[s].get_nowait()
                        except Queue.Empty:
                            # No message waiting to be sent, remove from list of connections waiting to send
                            outputs.remove(s)
                        else:
                            s.send(next_message)

                    # Handle connections with exceptions by closing them
                    for s in exceptional:
                        inputs.remove(s)
                        if s in outputs:
                            outputs.remove(s)
                        s.close()
                        del message_queues[s]

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
