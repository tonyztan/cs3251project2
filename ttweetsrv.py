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

# Sockets to check for incoming data
inputs = []

# Sockets to use for outgoing data
outputs = []

# Dictionary. Key: Connection. Value: Queue for outgoing data.
message_queues = {}

# List of tuples. [(Username, Connection, List of Hashtags)]
connected_users = []

# Connections that are about to be closed
connections_pending_termination = []


def usage():
    """
    Prints out usage information for the program and then exits.
    :return: none
    """

    print 'Error. Usage: ./ttweetsrv.py <ServerPort>'
    print 'ServerPort must be valid.'
    exit()


def find_user_by_username(username):
    for i in range(len(connected_users)):
        if username == connected_users[i][0]:
            return i
    return -1


def find_user_by_connection(connection):
    for i in range(len(connected_users)):
        if connection == connected_users[i][1]:
            return i
    return -1


def find_connections_by_hashtag(hashtag):
    connections = []
    for i in range(len(connected_users)):
        if hashtag in connected_users[i][2]:
            connections.append(connected_users[i][1])
    return connections


def add_user(username, connection):
    connected_users.append((username, connection, []))


def remove_user(user_index):
    del connected_users[user_index]


def subscribe(connection, hashtag):
    user_index = find_user_by_connection(connection)
    if len(connected_users[user_index][2]) < 3:
        if hashtag in connected_users[user_index][2]:
            return "Error: You are already subscribed to this hashtag."
        connected_users[user_index][2].append(hashtag)
        return "You have successfully subscribed to #" + hashtag
    return "Error: You are already subscribed to the maximum number of hashtags (3)."


def unsubscribe(connection, hashtag):
    user_index = find_user_by_connection(connection)
    if hashtag in connected_users[user_index][2]:
        connected_users[user_index].remove(hashtag)
        return "You have succesfully unsubscribed to #" + hashtag
    return "Error: You are not subscribed to #" + hashtag


def push_tweet(connection, tweet, hashtags):
    user_index = find_user_by_connection(connection)
    username = connected_users[user_index][0]
    tweet = username + ": " + tweet
    connections = []

    for i in range(len(connected_users)):
        for hashtag in hashtags:
            if "ALL" in connected_users[i][2] or hashtag in connected_users[i][2]:
                connections.append(connected_users[i][1])
                break

    for connection in connections:
        request_send(connection, tweet)

    if len(connections) == 0:
        return False
    return True


def request_send(connection, data):
    """
    Sends the specified data to the specified connection socket.
    It works by adding the information to the appropriate queues.
    :param connection: The connection to send to.
    :param data: The data to send.
    :return: none
    """
    data += '"""'
    message_queues[connection].put(data)
    if connection not in outputs:
        outputs.append(connection)


def handle_request(connection, request):
    """
    Handles the specified request from the specified connection.
    :param connection: The connection associated with the request.
    :param request: The request to handle.
    :return: none
    """
    if (len(request) > 13) and (request[0:13] == "set username "):
        # username logic
        requested_username = request[13:]
        if find_user_by_username(requested_username) != -1:
            request_send(connection, "Error: Username already taken. Please choose new username.")
            request_send(connection, "exit")
            request_close(connection)
        else:
            add_user(requested_username, connection)
            request_send(connection, "Your username is now: " + requested_username)
            request_send(connection, "command")

    elif (len(request) > 13) and (request[0:13] == "unsubscribe #"):
        # unsubscribe logic
        hashtag = request[13:]
        # if requested_unsubscribe_keyword in connected_users.get
        message = unsubscribe(connection, hashtag)
        request_send(connection, message)
        request_send(connection, "command")

    elif (len(request) > 11) and (request[0:11] == "subscribe #"):
        hashtag = request[11:]
        message = subscribe(connection, hashtag)
        request_send(connection, message)
        request_send(connection, "command")

    elif (len(request) > 7) and (request[0:7] == 'tweet "'):
        # tweet logic
        trimmed_request = request[7:]
        first_quote_index = trimmed_request.find('"')
        last_quote_index = trimmed_request.rfind('"')
        if first_quote_index != last_quote_index:
            request_send(connection, "Error: Content of tweet and hashtags must not contain a quote symbol.")
            request_send(connection, "command")
        else:
            tweet = trimmed_request[:first_quote_index]
            hashtags = trimmed_request[first_quote_index + 1:].split("#")[1:]
            if len(tweet) < 1 or len(hashtags) < 1:
                request_send(connection, "Error: Tweet and hashtag length must not be zero.")
                request_send(connection, "command")
            else:
                if push_tweet(connection, '"' + trimmed_request, hashtags):
                    request_send(connection, "Tweet sent successfully!")
                else:
                    request_send(connection,
                                 "Tweet not sent because no users are subscribed to the specified hashtags.")
                request_send(connection, "command")

    elif (len(request) == 8) and (request == "timeline"):
        # timeline logic (client is responsible for displaying timeline)
        request_send(connection, "command")

    elif (len(request) == 4) and (request == "exit"):
        # exit logic
        request_send(connection, "exit")
        request_close(connection)

    else:
        # invalid request logic
        request_send(connection, "Error: Invalid Command.")
        request_send(connection, "command")


def close_connection(connection):
    """
    Closes the specified connection and removes it from memory.
    :param connection: The connection to close.
    :return: none
    """
    if connection in inputs:
        inputs.remove(connection)
    if connection in outputs:
        outputs.remove(connection)
    connection.close()
    del message_queues[connection]

    user_index = find_user_by_connection(connection)
    if user_index >= 0:
        remove_user(user_index)


def request_close(connection):
    connections_pending_termination.append(connection)


# Consulted: https://pymotw.com/2/select/
def server(port):
    """
    Runs the server at the specified port.
    :param port: The port to run the server on.
    :return: none
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
                global inputs
                inputs = [server_socket]

                while inputs:
                    readable, writable, exceptional = select.select(inputs, outputs, inputs)

                    # Handle outgoing data
                    for s in writable:
                        try:
                            while True:
                                next_message = message_queues[s].get_nowait()
                                s.send(next_message)
                        except Queue.Empty:
                            # No message waiting to be sent, remove from list of connections waiting to send
                            outputs.remove(s)

                    # Handle connections that need to be closed
                    for s in connections_pending_termination:
                        close_connection(s)
                        if s in readable:
                            readable.remove(s)
                        if s in exceptional:
                            readable.remove(s)

                    # Handle incoming data
                    for s in readable:
                        # Handle server sockets that are waiting to accept a connection
                        if s is server_socket:
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
                                close_connection(s)

                    # Handle connections with exceptions by closing them
                    for s in exceptional:
                        close_connection(s)

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
    :return: none
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
