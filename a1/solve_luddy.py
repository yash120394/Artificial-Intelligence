#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: [yashkuma@iu.edu]
#
# Based on skeleton code by D. Crandall, September 2019
from queue import PriorityQueue
import queue as Q
import heapq
from heapq import heapify, heappush, heappop
import sys

# Initialise moves for ordinary, circular and l moves
o_moves = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
l_moves = { "A":(2,1),"B": (2,-1),"C":(-2,1),"D": (-2, -1),"E":(1,2),"F":(1,-2),"G": (-1,2),"H": (-1, -2) }


# function to return row, col to index number
def rowcol2ind(row, col):
    return row*4 + col

# function to return index number to row and column
def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

# check if index is within the board
def valid_index(row, col):
    return 0 <= row <= 3 and 0 <= col <= 3

# swap index of given two index numbers
def swap_ind(list, ind1, ind2):
    return list[0:ind1] + (list[ind2],) + list[ind1+1:ind2] + (list[ind1],) + list[ind2+1:]

# swap tiles to return the state
def swap_tiles(state, row1, col1, row2, col2):
    return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

# Printable board 
def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]

# return a list of possible successor states
def successors(state):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    if (sys.argv[2] == 'original'):
        return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) for (c, (i, j)) in o_moves.items() if valid_index(empty_row+i, empty_col+j) ]
    elif (sys.argv[2] == 'luddy'):
        return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) for (c, (i, j)) in l_moves.items() if valid_index(empty_row+i, empty_col+j) ]
    else:
        return [(swap_tiles(state, empty_row, empty_col, (empty_row + i) % 4, (empty_col + j) % 4), c) for (c, (i, j)) in o_moves.items()]

# check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0
    
# function to return heuristic value of given state i.e. number of misplaced tiles
def calculate_h(state):
    sum = 0
    for i in range(len(state)-1): 
        if state.index(i+1) != i: 
            sum += 1
    return sum 

# The solver! - using A* search right now
def solve(initial_board):
    visited = []
    q = []   
    heappush(q,(calculate_h(initial_board),initial_board, ""))
    while  len(q)>0:
        (h,state,route_so_far) = heappop(q)
        if is_goal(state):
            return(route_so_far)
        for (succ, move) in successors( state ):
            if succ in visited : continue
            visited.append(succ)
            heappush(q,(calculate_h(succ)+1,succ,route_so_far + move))
    return False


# check permuatation inversion of a state
def check_inversion(state):
    sum = 0 
    for i in range(len(state)):
        for j in range(i+1,len(state)):
            if (state[i] > state[j]):
                sum += 1
    if (sum%2) == 0:
        return True 
    else:
        return False


# test cases
if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise(Exception("Error: expected 2 arguments"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]


    if len(start_state) != 16:
        raise(Exception("Error: couldn't parse start state file"))    

    if(check_inversion(start_state) == 1):
        print("No solution")
    else:
        print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))
    
        print("Solving...")
        route = solve(tuple(start_state))
    
        print("Solution found in " + str(len(route)) + " moves:" + "\n" + route)
