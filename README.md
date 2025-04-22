# Simple Task Collab
a simple client server task dashboard for one off use (ie. not encrypted, probably buggy and overall pretty mid)

## Concept

- Server runs on a dashboard that displays the current task board, updating on 30 second intervals. Server saves off json for external use if need be.
- Clients can connect and update the board with new tasks and assign users.
- If you wanna just remotely see the board you can just send a tcp connect to the server, send `b\x90\x90\x90\x90`. It'll spit back a pickle of a dictionary of the board.

## Server usage
```
usage: ./stcollab_server.py [-h] [-p PORT] [-b BOARD]

Simple Collaboration Server

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  TCP port to listen on
  -b BOARD, --board BOARD
                        JSON Board to use
```

The server will save off its server as a backup by default in `/tmp/stcollab.board` but can be specified with -b anywhere

## Client usage
```
usage: ./stcollab_client.py [-h] [-s SERVER] [-p PORT]

Simple Collaboration Client

options:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Simple Collaboration Server Host
  -p PORT, --port PORT  Simple Collaboration Server Port

# After connecting to the server, client is presented with a input menu. Example
Connected to 127.0.0.1
CURRENT BOARD
        1. Example Task: In Progress
                - Chungus, Test

What would you like to do?
1) Add Task
2) Update Task
3) Remove Task
4) Assign/Remove Users
>1
Task Description:
Test Task
Task Completed (Y/n): n
NEW BOARD
        1. Example Task: In Progress
                - Chungus, Test
        2. Test Task: In Progress

```
