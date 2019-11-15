# a0
# part 1 
 
- Intially, the code was using stack concept which was going on a infinite loop. Due to this the code was not able give the solution. 
- The solution to this problem was implemented using queue concept using pop(0) which is FIFO Data Structure
- The display of the path was implemented in the moves function where the input parameters where map, row and column. With possible moves, directions along with moves were added and returned if it was a valid move. 
- The search function is defined such that if fringe length is 0, then return solution is infinite. Already visited nodes has not been considered for succesor states. 
-  In the search function, created fringe with location, distance and direction and returned direction along with distance if it reaches goal state. 

#Sample code for implementation of direction
```
def moves(map, row, col):
	moves=((row+1,col,'S'), (row-1,col,'N'), (row,col-1,'W'), (row,col+1,'E'))
# Return only moves that are within the board and legal (i.e. on the sidewalk ".")
	return [move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@")]
```
#Sample code for search function
```
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
```

#part 2

- Intially it was placing friends in random places without checking if two friends can see each other.
- The solution to this problem was implmented by creating a check function which checks if at a particular position a friend can be placed or not. The board was converted into array because accessing the rows and columns is possible in the array data type.If a row and column does not contain 'F', return true. If not, create a list containing rows above and below and columns left and right. Check either the list is empty or does not contain 'F' at the nearest position from current position after removing sidewalks from the list. If the condition satisfy, return true else false.

#Sample code for check function
#Check if a friend can be added in board at row, column
```
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
 ```
- Return add friend on successors function if check function satisfy. 

# Modified code for successor function    
# Get list of successors of given board state
```
def successors(board):
    return [ add_friend(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if check(board, r,c)]
```
- In the solve function, already visited nodes has not been considered for succesor states.

# Modified code for solve function
# Solve n-rooks! 
# Check for visited nodes
```
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
```

- Running time is also added in the main function

- Initial state is board with no friends in it.
- State space is all arrangements of k = 0,1,2,...8,9 such that no two friends can see each other
- Succesor function is obtained by adding one friend in a location such that no two friends can see each other
- Goal state is adding k friends in the board such that no two friends can see each other.   
- Stack concept of Data Structure has been used for search.   


 