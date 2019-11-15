# a1

# The Luddy Puzzle 

## Inititalising moves for original, luddy and circular moves
```
o_moves = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
l_moves = { "A":(2,1),"B": (2,-1),"C":(-2,1),"D": (-2, -1),"E":(1,2),"F":(1,-2),"G": (-1,2),"H": (-1, -2) }
```

## Created succesors of the state for each of the three moves possible : original, luddy and circular. 
```
def successors(state):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    if (sys.argv[2] == 'original'):
        return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) for (c, (i, j)) in o_moves.items() if valid_index(empty_row+i, empty_col+j) ]
    elif (sys.argv[2] == 'luddy'):
        return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) for (c, (i, j)) in l_moves.items() if valid_index(empty_row+i, empty_col+j) ]
    else:
        return [(swap_tiles(state, empty_row, empty_col, (empty_row + i) % 4, (empty_col + j) % 4), c) for (c, (i, j)) in o_moves.items()]
```

## Created heuristic function to calculate h value of a given state
- Heuristic function is optimal for original, luddy and circular moves using number of misplaced tiles as heuristic function
```
def calculate_h(state):
    sum = 0
    for i in range(len(state)-1): 
        if state.index(i+1) != i: 
            sum += 1
    return sum 
```

# Solved function using A* search algorithm
- Used heap push method to pop state which has the lowest f i.e. h(s) + c(s)
- h(s) is heuristic function and c(s) is cost of each move
- Revisited state has not been considered as it leads to high computational expense



```
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
```

# Check permutation inversion of board 
```
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
```



