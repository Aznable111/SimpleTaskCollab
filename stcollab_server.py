#!/usr/bin/env python3

import socket
import threading
import argparse
import sys
import os
import json
import time
import pickle

board={}
startup=True
"""
### EXAMPLE BOARD DICT
{
    "1" : ["Complete writing this thing", "False"],
    "2" : ["Tbh idk man", "True"]
}
"""
board_file={}
#term_clear = b'\x1b\x5b\x48\x1b\x5b\x5a\x1b\x5b\x33\x4a'.decode()

def print_board(b):
     for task in b:
        print(task, end=". ")
        print(b[task][0],end=": ")
        if(b[task][1] == "True"):
            print("Completed")
        else:
            print("In Progress")
        if (len(b[task][2]) > 0):
            print("\t- ",end="")
            user_pos = 0
            for user in b[task][2]:
                user_pos += 1
                if user_pos == len(board[task][2]):
                    print(user,end="")
                elif len(board[task][2]) >1:
                    print(user,end=", ")
            print()


def display_board(bp):
    global board
    global startup
    while True:
        try:
            fp = open(bp,'r')
            board_file = json.load(fp)
            fp.close()
        except:
            pass

        # Check the live board in memory for new items
        if startup == True:
            board = board_file
            startup = False
        elif board_file != board:
            board_file = board
            try:
                fp = open(bp,'w')
                json.dump(board_file,fp)
                fp.close()
            except:
                pass

        """
        Old modification system
        for task in board:
            if task not in board_file:
                board_file[task] = board[task]

        # Check the board on disk for items that were removed or changed
        for task in board_file:
            # Task was removed
            if task not in board:
                del board_file[task]
            else:
                # If task was renamed change it to current completely
                if board[task][0] != board_file[task][0]:
                    board_file[task] = board_file[task]
                # If task completion changed set it
                elif board[task][1] != board_file[task][1]:
                      board_file[task][1] = board[task][1]
        """
        # Finally display the board then write
        os.system('clear')
        print("TASKS:")
        print_board(board_file)

        time.sleep(30)



def connection_thread(sock):
    global board
    while True:
        conn, addr = sock.accept()
        data = conn.recv(4096)
        if data == b'\x90\x90\x90\x90':
            board_send_data = pickle.dumps(board)
            conn.sendall(board_send_data)
        else:
            conn.close()
        data = conn.recv(65535)
        if(data == b'\x99\x99'):
            conn.close()
        elif(data == b''):
            conn.close()
        else:
            try:
                board = pickle.loads(data)
            except:
                print(f'Error recieving board update, recieved: {data}')

            conn.close()
    

def setup_server(port,board_path):
    global board
    if not os.path.isfile(board_path):
        print(f"Board File: {board_path} not found, creating file")
        board = { "1": [ "Example Task", "False", [] ] }
        fp = open(board_path, 'w')
        json.dump(board, fp)
        fp.close()

    try:
        fp = open(board_path, 'r')
        board = json.load(fp)
        fp.close()
    except Exception as e:
        print(f"Error opening file {board_path}: {e}")
        sys.exit(1)

    s = socket.socket()
    s.bind(('0.0.0.0', port))
    s.listen()
    
    conn_thread = threading.Thread( target=connection_thread, args=(s, ) )
    board_thread = threading.Thread( target=display_board, args=(board_path, ) )

    conn_thread.start()
    board_thread.start()
    try:
        board_thread.join()
    except KeyboardInterrupt:
        s.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser(prog=f'{sys.argv[0]}',
                                description='Simple Collaboration Server'
                                )
    p.add_argument('-p','--port',help='TCP port to listen on', default='55554')
    p.add_argument('-b','--board',help='JSON Board to use', default='/tmp/stcollab.board')
    args = p.parse_args()
    setup_server(int(args.port),args.board)
