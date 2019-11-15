#!/usr/local/bin/python3
#
# hide.py : a simple friend-hider
#
# Submitted by : [Yash Kumar, yashkuma@iu.edu]
#
# Based on skeleton code by D. Crandall and Z. Kachwala, 2019
#
# The problem to be solved is this:
# Given a campus map, find a placement of F friends so that no two can find one another.

import sys
import numpy as np
import time

# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().split("\n")]

# Count total # of friends on board
def count_friends(board):
    return sum([ row.count('F') for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a friend to the board at the given position, and return a new board (doesn't change original)
def add_friend(board, row, col):
    return board[0:row] + [board[row][0:col] + ['F',] + board[row][col+1:]] + board[row+1:]

#Check if a friend can be added in board at row, column
def check(board, r, c):
    if board[r][c] == '.':
        board_array = np.array(board)
        if (('F' not in board_array[r,:]) and ('F'not in board_array[:,c])):
           return True       
        else:
            list_r1 = board_array[r,:c].tolist()
            list_r2 = board_array[r,c+1:].tolist() 
            list_c1 = board_array[:r,c].tolist()
            list_c2 = board_array[r+1:,c].tolist()
            list_r1[:] = (value for value in list_r1 if value != '.')
            list_r2[:] = (value for value in list_r2 if value != '.')
            list_c1[:] = (value for value in list_c1 if value != '.')
            list_c2[:] = (value for value in list_c2 if value != '.')
            if (len(list_r1) == 0 or list_r1[-1] != 'F') and (len(list_r2) == 0 or list_r2[0] != 'F') and (len(list_c1) == 0 or list_c1[-1] != 'F') and (len(list_c2) == 0 or list_c2[0] != 'F'):
                return True
    return False


# Get list of successors of given board state
def successors(board):
    return [ add_friend(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if check(board, r,c)]

# check if board is a goal state
def is_goal(board):
    return count_friends(board) == K 

# Solve n-rooks! 
# Check for visited nodes
visited = []
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors( fringe.pop() ):
            if s in visited : continue
            visited.append(s)
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

# Main Function
if __name__ == "__main__":
    IUB_map=parse_map(sys.argv[1]) 
    # This is K, the number of friends
    K = int(sys.argv[2]) 
    print ("Starting from initial board:\n" + printable_board(IUB_map) + "\n\nLooking for solution...\n")
    start = time.process_time()
    solution = solve(IUB_map)
    # your code here    
    print(time.process_time() - start)
    print ("Here's what we found:")
    print (printable_board(solution) if solution else "None")