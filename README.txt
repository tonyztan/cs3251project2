////////////////////////////////////////////////////////////////////////////////
// General Information                                                        //
////////////////////////////////////////////////////////////////////////////////
Authors: Matthew Wang (mwang400@gatech.edu) and Tony Tan (tonytan@gatech.edu)

Class name: CS-3251-A (Note: Tony Tan is in section B, but this assignment was
completed based on the requirements of section A.
See "3251 Project 2 - Spring 2019.pdf" for details.)

Date: 04/13/2019

Assignment: Programming Assignment 2

Included files: 
"3251 Project 2 - Spring 2019.pdf"      Project description
README.txt                              README document
Sample.txt                              Inputs and outputs of test scenarios
ttweetcli.py                            The python file for the clients
ttweetsrv.py                            The python file for the server

////////////////////////////////////////////////////////////////////////////////
// Instructions                                                               //
////////////////////////////////////////////////////////////////////////////////
Running Server:
The server is written in python2 and can be run from the command line by 
navigating to the folder containing the ttweetsrv.py file and typing the 
following command:
./ttweetsrv.py <ServerPort>

Running Client:
The client is written in python2 and can be run from the command line by 
navigating to the folder containing the ttweetcli.py file and typing the 
following command:
./ttweetcli.py <ServerIP> <ServerPort> <Username>

////////////////////////////////////////////////////////////////////////////////
// Implemenation Details                                                      //
////////////////////////////////////////////////////////////////////////////////
Work Distribution:
Matthew wrote the client program, except for the code that verifies IP addresses
and port numbers are formatted correctly. In the server, he wrote the code in
the handle_request() function that dealt with usernames and hashtags, as well as
the following helper functions: add_user(), remove_user(), subscribe(), 
unsubscribe(), push_tweet_to_clients(), find_user_by_username(), 
find_user_by_connections(), and find_connections_by_hashtag(). He also drafted
the README.txt and Sample.txt files. 

Tony wrote the code in the client that verifies IP addresses and port numbers.
He designed the overall structure of the server program and the protocol between
the server and client and wrote the code that handled connections with clients 
and the code in the handle_request() function that dealt with parsing tweets 
and clients that were either viewing their timelines or exiting, as well as the 
following helper functions: request_send(), request_close(), 
and close_connection().
--------------------------------------------------------------------------------
Implementation and Protocol Description:
As suggested in the project description, the server uses select to maintain 
connections with multiple clients. The server is responsible for understanding 
and handling requests from the clients since the clients send user commands 
directly to the server without modifying them. The server is also responsible
for telling the client what it should do next. The client is responsbile for 
locally storing tweets and displaying them when requested by the user, sending 
user commands to the server, and displaying messages from the server to its
user.

In our protocol, the server can send the client the following messages:
"command": The server tells a client it is ready for a request, so the client 
should prompt its user for another command.

"tweet <author>: <full tweet with hashtags>": The server sends tweets to all
subscribed users for clients to store and show their users.

"exit": The server tells the client to stop running.

"<message>": Any message that does not fall under one of the categories above is
a message to the user that the client is expected to display.

The client can send the server the following messages:
"set username <username>": This message is sent when the client starts running
to login under the requested username.

"<command>": Any other message is a command provided by the user which is sent
to the server to be handled.