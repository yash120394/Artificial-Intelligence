# Sliding tile game

## Step 1
- Creation of heuristic function which evaluate the current state of the tile
- The heuristic function used is difference of weighted sum of letters of max and min present in the current state
- Weight has been given in the order of letter K = 11, J =10, I = 9, H = 8,  G = 7, F = 6, E = 5, D = 4, C = 3, B = 2, A = 1
- For ex : If current state has 2 A's and 3 B's of max and 1 A's and 4 B's of min, then 
  h = 1*(2-1) + 2*(3-4)
```
def heuristics(board):
    board1 = list(itertools.chain(*board))
    player = sys.argv[1]
    if player == 'ai':
        h = 1*(board1.count('A')-board1.count('a'))+2*(board1.count('B')-board1.count('b'))+3*(board1.count('C')-board1.count('c'))+4*(board1.count('D')-board1.count('d'))+5*(board1.count('E')-board1.count('e'))+6*(board1.count('F')-board1.count('f'))+7*(board1.count('G')-board1.count('g'))+8*(board1.count('H')-board1.count('h'))+9*(board1.count('I')-board1.count('i'))+10*(board1.count('J')-board1.count('j'))+11*(board1.count('K')-board1.count('k'))
        return h
    if player == 'human':
        h = 1*(board1.count('a')-board1.count('A'))+2*(board1.count('b')-board1.count('B'))+3*(board1.count('c')-board1.count('C'))+4*(board1.count('d')-board1.count('D'))+5*(board1.count('e')-board1.count('E'))+6*(board1.count('f')-board1.count('F'))+7*(board1.count('g')-board1.count('G'))+8*(board1.count('h')-board1.count('H'))+9*(board1.count('i')-board1.count('I'))+10*(board1.count('j')-board1.count('J'))+11*(board1.count('k')-board1.count('K'))
        return h
```

## Step 2
- Used recursion for creating max play, min play and next move function
- Initialise the best utility value for max as -infinity and min as +infinity which is the worst they can get
- Used depth = 6 for evaluating the heuristic function
- Used alpha and beta parameters in min and max play to discontinue the search below if alpha > beta
- For max, the alpha value is max of alpha and best utility we get from one move
- For min, the alpha value is min of alpha and best utility we get from one move 
- Alpha has been initialised as -infinity and beta as +infinity

Sample code for min and max play 
```
# Implemented alpha beta pruning
# define min play and return best move while searching till depth = 6 for min 
def min_utility(game: Game_IJK,d,alpha,beta):
    d = d + 1
    state = game.state()
    board = game.getGame()
    moves = ['U', 'D', 'L', 'R']
    best_utility = float('inf')
    if state == 'K' or state == 'k' or state == 'tie' or d == 6:
        return heuristics(board)
    for move in moves:
        clone = game.makeMove(move)
        utility = max_utility(clone,d,-float('inf'),float('inf'))
        if utility < best_utility:
            best_move = move
            best_utility = utility
            beta = min(beta,best_utility)
            if beta <= alpha:
                break
    return best_utility

# define max play and return best move while searching til depth = 6 for max
def max_utility(game: Game_IJK,d,alpha,beta):
    d = d + 1
    state = game.state()
    board = game.getGame()
    if state == 'K' or state == 'k' or state == 'tie' or d == 6:
        return heuristics(board)
    moves = ['U', 'D', 'L', 'R']
    best_utility = float('-inf')
    for move in moves:
        clone = game.makeMove(move)
        utility = min_utility(clone,d,-float('inf'),float('inf'))
        if utility > best_utility:
            best_move = move
            best_utility = utility
            alpha = max(alpha,best_utility)
            if beta <= alpha:
                break
    return best_utility
    
```

# Challenges
- Since the number of states from initial to goal state is very large, we cannot use minimax algorithm for expanding the whole tree, so we implemented the depth limited minimax. 
- After implementing depth limited minimax, the computational time was large for depth = 6. In order to reduce the computational time, we used alpha beta pruning which reduced the computational time significantly
