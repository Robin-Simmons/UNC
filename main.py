# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 22:22:38 2020

@author: Robin
"""
import os

import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output

class game_state:
    def __init__(self):
        
        self.board = np.zeros([9,9])
        #self.board[0:3,3] = np.ones(3)
        #self.board[0:3, 0:3] = diagonal
        self.meta_board = np.zeros([3,3])
        self.last_move = np.array([np.nan, np.nan]) #last_move being nan means
        self.current_player = 1
        # any sub game can be choosen
    def check_board(self, board, player):
        diagonal = np.zeros([3,3])
        for i in range(3):
            diagonal[i,i] = 1
        
        diagonal_reverse = np.flip(diagonal, axis = 0)
        if np.array_equal(board, player*diagonal) == True or np.array_equal(board, player*diagonal_reverse) == True:
            return True 
        for k in range(3):
                        
            if np.array_equal(board[k,:], player*np.ones(3)) == True or np.array_equal(board[:,k], player*np.ones(3)) == True:
                return True
        return False
    
    def check_win(self):
        #print(self.board)
        
        for player in [-1,1]:
            for i in range(3):
                for j in range(3):
                    sub_game = self.board[i*3:i*3+3,j*3:j*3+3]
                    if self.check_board(sub_game, player) == True and self.meta_board[i,j] == 0:
                        self.last_move = np.array([np.nan, np.nan])
                        self.meta_board[i,j] = player
                    
    def check_move_legal(self, sub_game, move):
        # numpy nans evaluate to True 
        
        if self.board[int(sub_game[0]*3 + move[0]), int(sub_game[1]*3 + move[1])] == 0:
            print("legal move")
        else:
            print("illegal move")
            
    def make_move(self):
        if self.current_player == 1:
            print("X's move")
        else:
            print("O's move")
        # moves are in format (i,j,k,l), with ij refering to which sub game
        # and k,l refering to pos within chosen sub game 
        print(self.last_move)
        if np.all(np.isnan(self.last_move)) == True:
            sub_game = np.fromstring(input("Sub game: "), sep = ",")
            #print(sub_game)
        else:
            sub_game = self.last_move
        move = np.fromstring(input("Move within sub game {}: ".format(sub_game)), sep = ",")
        self.check_move_legal(sub_game, move)
        self.board[int(sub_game[0]*3 + move[0]), int(sub_game[1]*3 + move[1])] = self.current_player
        self.last_move = move
        self.check_win()
        self.current_player = -1*self.current_player
def player_str(player):
    if player == 0:
        return " "
    elif player == 1:
        return "X"
    else:
        return "O"
def drawboard(board):
    x_win = np.array([[1,0,1],[0,1,0],[1,0,1]])
    o_win = np.array([[-1,-1,-1],[-1,0,-1],[-1,-1,-1]])
    for i in range(9):
        if i == 3 or i == 6:
            print("============#===========#============")
        else:
            print("------------#-----------#------------")
        substring = ""
        for j in range(9):
            
            if game.meta_board[i//3,j//3] == 1:
                
                fill = x_win[i%3,j%3]
            elif game.meta_board[i//3,j//3] == -1:
                fill = o_win[i%3,j%3]
            else:
                fill = board[i,j]
            fill = player_str(fill)
            if j == 3 or j == 6:
                divider = "#"
            else:
                divider = "|"
            if board[i,j] == 0:
                substring = "{}{} {} ".format(substring, divider, fill)
            elif board[i,j] == 1:
                substring = "{}{} {} ".format(substring, divider, fill)
            else:
                substring = "{}{} {} ".format(substring, divider, fill)
            #print(game.meta_board[i//3,j//3])
            
        print(substring + "|")
        
        #print("{}{}{}||{}{}{}||{}{}{}".format(int(board[0,i]),int(board[1,i]),int(board[2,i]),int(board[3,i]),int(board[4,i]),int(board[5,i]),int(board[6,i]),int(board[7,i]),int(board[8,i])))
    print("------------#-----------#------------")
game = game_state()
board = game.board


drawboard(game.board)
    #game.make_move()
