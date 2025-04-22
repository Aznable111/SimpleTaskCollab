#!/usr/bin/env python3
import socket
import argparse
import sys
import pickle
import json

board = {}

def print_board(board):
    for task in board:
        print(f'\t{task}', end='. ')
        print(board[task][0], end=': ')
        if board[task][1] == "True":
            print("Completed")
        else:
            print("In Progress")
        if len(board[task][2]) > 0:
            print("\t\t- ",end="")
            user_pos = 0
            for user in board[task][2]:
                user_pos += 1
                if user_pos == len(board[task][2]):
                    print(user,end="")
                elif len(board[task][2]) > 1:
                    print(user,end=", ")        
                
            print()

def main(server,port):
    global board
    try:
        s=socket.socket()
        s.connect((server,port))
    except ConnectionRefusedError:
        print("Cannot Connect to server.")
        s.close()
        sys.exit(1)
    print(f"Connected to {server}")
    s.send(b'\x90\x90\x90\x90') # Magic, to get the current board
    rb_data = s.recv(65535)
    try:
        board = pickle.loads(rb_data)
    except:
        print(f"Board data could not be unpickled. Recvd data: {rb_data}")
        s.close()
        sys.exit(1)

    print("CURRENT BOARD")
    print_board(board)

    print()
    print("What would you like to do?")
    print("1) Add Task")
    print("2) Update Task")
    print("3) Remove Task")
    print("4) Assign/Remove Users")
    a = input('>')
    if a == "1":
        desc = input("Task Description:\n")
        while True:
            status = input("Task Completed (Y/n): ")
            if status.lower() not in "yn":
                print("Not valid")
                continue
            break
        if status.lower() == "n":
            status = "False"
        elif status.lower() == "y":
            status = "True"
        task_index = 0 
        for task in board:
            if int(task) > task_index:
                task_index = int(task)
        task_index = str(int(task_index) + 1)
        board[task_index] = [ desc, status, [] ]
    elif a == "2":
        while True:
            index = input("Which task id?: ")
            if index not in board.keys():
                print("Invalid task id")
                continue
            else:
                desc = input("New description (enter to leave the same):")
                if(desc == ""):
                    desc = board[index][0]
                status = input("Task Completed (Y/n) ")
                if status.lower() == "n":
                    status = "False"
                elif status.lower() == "y":
                    status = "True"
                else:
                    status = board[index][1]
                board[index] = [ desc, status, [] ]
            break
        
    elif a == "3":
        while True:
            index = input("Which task id?: ")
            if index not in board.keys():
                print("Invalid task id")
                continue
            break

        new_board = {}
        for task in board:
            if task == str(index):
                continue
            elif int(task) > int(index):
                new_id = str(int(task)-1)
            else:
                new_id = task
            new_board[new_id] = board[task]
        board = new_board
    elif a == "4":
        while True:
            print("1) Assign User")
            print("2) Remove User")
            b = input('>')
            if b not in '12' and len(b) != 1:
                print("Invalid Selection")
                continue
            break
        if b == '1':
            while True:
                index = input("Which task id?: ")
                if index not in board.keys():
                    print("Invalid task id")
                    continue
                break
            name = input("What user? ")
            board[index][2].append(name)

        elif b == '2':
            while True:
                index = input("Which task id?: ")
                if index not in board.keys():
                    print("Invalid task id")
                    continue
                break
            if len(board[index][2]) == 0:
                print("No user to remove, exiting...")
                s.sendall(b"\x99\x99")
                s.close()
                sys.exit(0)
            else:
                i = 1 
                while i <= len(board[index][2]):
                    print(f'{i}. {board[index][2][i-1]}')
                    i+=1
                u_num = input('Which user number? ')
                while True:
                    try:
                        u_num = int(u_num)
                    except:
                        print("Input is not an integer")
                        continue
                    if u_num > len(board[index][2]) or u_num <= 0:
                        print("Not valid selection")
                        continue
                    break
                board[index][2].pop(u_num-1)

                    

    else:
        print("Exiting...")
        s.sendall(b"\x99\x99")
        s.close()
        sys.exit(0)
    print("NEW BOARD")
    print_board(board)
    print('\n')
    s.sendall(pickle.dumps(board))
    s.close()




if __name__ == "__main__":
    p = argparse.ArgumentParser(
            prog=f'{sys.argv[0]}',
            description='Simple Collaboration Client'
            )
    p.add_argument('-s','--server',help='Simple Collaboration Server Host',default='127.0.0.1')
    p.add_argument('-p','--port',help='Simple Collaboration Server Port',default='55554')
    args = p.parse_args()
    main(args.server,int(args.port))

