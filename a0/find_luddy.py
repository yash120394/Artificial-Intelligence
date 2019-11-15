#!/usr/local/bin/python3
#
# find_luddy.py 
#
# Submitted by : [Yash Kumar, yashkuma@iu.edu]
#python3 /u/yashkuma/yashkuma-a0/find_luddy.py /u/yashkuma/yashkuma-a0/map.txt 

import sys
import json
import collections
import time

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().split("\n")]


# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
	return 0 <= pos[0] < n  and 0 <= pos[1] < m


# Find the possible moves and direction from position (row, col)
def moves(map, row, col):
	moves=((row+1,col,'S'), (row-1,col,'N'), (row,col-1,'W'), (row,col+1,'E'))
# Return only moves that are within the board and legal (i.e. on the sidewalk ".")
	return [move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@")]

# Perform BFS search on the map and check for visted nodes
visited = []
def search1(IUB_map):
	# Find my start position
	you_loc=[(row_i,col_i) for col_i in range(len(IUB_map[0])) for row_i in range(len(IUB_map)) if IUB_map[row_i][col_i]=="#"][0]
	fringe=[(you_loc,0,'')]
	while len(fringe) > 0:
		(curr_move, curr_dist, mov_dir)=fringe.pop(0)
		for move in moves(IUB_map, curr_move[0],curr_move[1]):
			if move in visited : continue
			visited.append(move)
			if IUB_map[move[0]][move[1]]=="@":
				return curr_dist+1, mov_dir+move[2]
			else:
				fringe.append((move, curr_dist + 1, mov_dir+move[2]))
	return 'Inf'


# Main Function
if __name__ == "__main__":
	IUB_map=parse_map(sys.argv[1]) 
	print("Shhhh... quiet while I navigate!")
	start = time.process_time()
	solution = search1(IUB_map)
	print(time.process_time() - start)
	if solution == 'Inf':
		print(solution)
	else:
		print("Here's the solution I found:")
		print(solution[0],solution[1])