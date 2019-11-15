#!/usr/local/bin/python3

"""
This is where you should write your AI code!

Author: [yashkuma@iu.edu]

Based on skeleton code by Abhilash Kuhikar, October 2019
"""

from logic_IJK import Game_IJK
import random
import itertools
import sys

# Suggests next move to be played by the current player given the current game
#
# inputs:
#     game : Current state of the game 
#
# This function should analyze the current state of the game and determine the 
# best move for the current player. It should then call "yield" on that move.


# logic code inspired from https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/

# define a heuristic function to evaluate state of a player
def heuristics(board):
    board1 = list(itertools.chain(*board))
    player = sys.argv[1]
    if player == 'ai':
        h = 1*(board1.count('A')-board1.count('a'))+2*(board1.count('B')-board1.count('b'))+3*(board1.count('C')-board1.count('c'))+4*(board1.count('D')-board1.count('d'))+5*(board1.count('E')-board1.count('e'))+6*(board1.count('F')-board1.count('f'))+7*(board1.count('G')-board1.count('g'))+8*(board1.count('H')-board1.count('h'))+9*(board1.count('I')-board1.count('i'))+10*(board1.count('J')-board1.count('j'))+11*(board1.count('K')-board1.count('k'))
        return h
    if player == 'human':
        h = 1*(board1.count('a')-board1.count('A'))+2*(board1.count('b')-board1.count('B'))+3*(board1.count('c')-board1.count('C'))+4*(board1.count('d')-board1.count('D'))+5*(board1.count('e')-board1.count('E'))+6*(board1.count('f')-board1.count('F'))+7*(board1.count('g')-board1.count('G'))+8*(board1.count('h')-board1.count('H'))+9*(board1.count('i')-board1.count('I'))+10*(board1.count('j')-board1.count('J'))+11*(board1.count('k')-board1.count('K'))
        return h

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

# Using minimax algorithm with alpha beta pruning, returns the best move for max given current state
def next_move(game: Game_IJK):
    '''board: list of list of strings -> current state of the game
       current_player: int -> player who will make the next move either ('+') or -'-')
       deterministic: bool -> either True or False, indicating whether the game is deterministic or not
    '''
    board = game.getGame()
    player = game.getCurrentPlayer()
    deterministic = game.getDeterministic()

    # You'll want to put in your fancy AI code here. For right now this just 
    # returns a random move.

    moves = ['U', 'D', 'L', 'R']
    best_move = moves[0]
    best_utility = float('-inf')
    for move in moves:
        clone = game.makeMove(move)
        utility = min_utility(clone,0,-float('inf'),float('inf'))
        if utility > best_utility:
            best_utility = utility
            best_move = move
    yield best_move
