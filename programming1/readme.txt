Tony Tan <tonytan@gatech.edu>
CS-3251-B Computer Networks I
February 14, 2019
Programming Assignment 1

Files submitted:
    - ttweetcli.py: Trivial Twitter application client.
    - ttweetsrv.py: Trivial Twitter application server.
    - readme.txt: README file.
    - sample.txt: Program output for test scenario.
    - LICENSE.txt: MIT Copyright License

To compile and run the client and server programs:
    - Programs are written in python so no manual compilation is required.
    - To run server:
        ./ttweetsrv.py <ServerPort>
            For example: ./ttweetsrv.py 13500
        ServerPort must be valid.

    - To run client:
        To upload: ./ttweetcli -u <ServerIP> <ServerPort> "<Message>"
            For example: ./ttweetcli -u 127.0.0.1 13500 "Hello World"
        To download: ./ttweetcli -d <ServerIP> <ServerPort>
            For example: ./ttweetcli -d 127.0.0.1 13500
        ServerIP and ServerPort must be valid, and Message must be 150 characters or less.

For output sample showing the result of running the test scenario above, please see sample.txt.

Protocol description:
    The protocol runs on top of TCP.

    (1) When a client intends to download a message from the server, the client opens a connection with the server.
    The client then sends "download=" as a string through the connection.
    Upon receiving the "download=" string, the server responds by sending the stored message through the connection.
    The client receives the message. Then the connection is closed.

    (2) When a client intends to upload a message to the server, the client opens a connection with the server.
    The client then prepends "upload=" to the message, and then it sends the resulting string through the connection.
    The server accepts and stores the message. Then the connection is closed.
    Optionally, the client may follow the download procedure described in (1) to verify the message stored at the sever.

Any known bugs or limitations:
    The server can only handle one client at a time, as specified by the assignment.
    There are no other known bugs or limitations.
