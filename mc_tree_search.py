# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 00:30:37 2020

@author: Robin
"""
import copy
import time

import numpy as np
import main
from anytree import Node, RenderTree
#0.0022916666666666667
#upper confidence bound for node
def UCB(V,N,n):
    if n == 0:
        return np.inf
    else:
        return V + 2*np.sqrt(np.log(N)/n)

def rollout(roll_node):
    #simulate game starting from leaf node state (roll node)
    rollout_game = main.game()
    rollout_game.board = roll_node.state
    sub_game = np.fromstring(roll_node.name, sep = ",").astype(int)
    #if subgame has been won/drawn already, randomly chose a new subgame
    
   
    game_cont = True
    while game_cont == True:
        if rollout_game.meta_board[sub_game[0], sub_game[1]] != 0:
            allowed_games  = np.argwhere(rollout_game.meta_board == 0)
            sub_game = allowed_games[np.random.choice(allowed_games.shape[0])]
        sub_board = rollout_game.board[sub_game[0]*3:sub_game[0]*3+3, sub_game[1]*3:sub_game[1]*3+3]
        #creates list of allowed moves that the monte carlo search can choose
        allowed_moves  = np.argwhere(sub_board == 0)
        #randomly chooses move (seems a bit hacky, must be a better way...)
        move = allowed_moves[np.random.choice(allowed_moves.shape[0])]
        rollout_game.board[sub_game[0]*3+move[0], sub_game[1]*3+move[1]] = rollout_game.player
        game_cont, winner = rollout_game.iterate_rollout(move, sub_game)
        sub_game = move
        
    return winner


def create_tree(game):
    #root is the current game state
    root = Node("root", parent=None, t = 0, n = 0, state = copy.deepcopy(game.board))
    
    #create a child for each possible move (9-filled squares)
    for i in range(3):
        for j in range(3):
            board = copy.deepcopy(game.board)
            last_move = game.last_move
            if game.check_move_legal(last_move, [i,j]) == True:
                board[int(last_move[0]*3 + i), int(last_move[1]*3 + j)] = -1
                Node("{},{}".format(i,j), parent = root, t = 0, n = 0, state = board)
    #set ucb for all leaf nodes
    ucb = np.ones(len(root.children))*np.inf
    for i in range(40):
        arg = np.argmax(ucb)
        roll_node = copy.deepcopy(root.children[arg])
        
        score = rollout(roll_node)
        root.children[arg].t = score
        root.children[arg].n += 1
        root.children[arg].parent.n += 1
        for ancestor in root.children[arg].ancestors:
            ancestor.t = score
        ucb[arg] = UCB(root.children[arg].t, root.children[arg].n, root.children[arg].parent.n)
        
    return np.fromstring(root.children[np.argmax(ucb)].name, sep = ",")
#X is player
#O is AI
#X starts
game = main.game()
main.drawboard(game)
for i in range(20):
    if game.player == 1:
        game.iterate_game()
    else:
        move = create_tree(game).astype(int)
        print(move)
        game.iterate_ai(move, game.last_move)
    main.drawboard(game)
