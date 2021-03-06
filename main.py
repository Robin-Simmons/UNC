# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 22:22:38 2020

@author: Robin
"""

import numpy as np


class game:
    def __init__(self):
        self.board = np.zeros([9,9]) #complete state of board
        self.meta_board = np.zeros([3,3]) #state of overall game (eg who was control
        # of the 9 subs games)
        self.last_move = np.array([np.nan, np.nan]) #when nan, next move can be anywhere
        self.player = 1 #X always starts
        
        
    def check_game_won(self, board):
        # creates arrays with filled diagonal
        diagonal = np.zeros([3,3])
        for i in range(3):
            diagonal[i,i] = 1
        diagonal_reverse = np.flip(diagonal, axis = 0)
        
        #checks if player has filled either diagonals
        if np.array_equal(board, self.player*diagonal) == True or np.array_equal(board, self.player*diagonal_reverse) == True:
            return self.player 
        
        #checks if player has filled any rows or columns
        for k in range(3):
                        
            if np.array_equal(board[k,:], self.player*np.ones(3)) == True or np.array_equal(board[:,k], self.player*np.ones(3)) == True:
                return self.player
        #checks if game is a draw
        if 0 not in board:
            return np.nan
        #returns 0 if game has not been won and if the game is not a draw
        else:
            return 0
    
    def check_move_legal(self, sub_game, move):
        #checks move is on board
        if move[0] not in np.arange(0,9) or move[1] not in np.arange(0,9):
            print("Not a valid location")
            return False
        #checks pos has not been filled already
        if self.board[int(sub_game[0]*3 + move[0]), int(sub_game[1]*3 + move[1])] != 0:
            print("Loc already taken")
            return False
        return True
    
    def make_move(self):
        print("{}'s move.".format(player_str(self.player)))
        move_legal = False
        while move_legal == False:
            if np.all(np.isnan(self.last_move)) == True:
                #if free move, let player chose from the free subgames
                free_game = False
                while free_game == False:
                    sub_game = np.fromstring(input("Subgame "), sep = ",").astype(int)
                    
                    if self.meta_board[sub_game[0],sub_game[1]] == 0:
                        free_game == True
                        break
                    else:
                        print("This subgame has been won already")
            else:
                sub_game = self.last_move
            #checks if move is legal
            move = np.fromstring(input("Move within subgame {} ".format(sub_game)), sep = ",").astype(int)
            move_legal = self.check_move_legal(sub_game, move)
        self.board[int(sub_game[0]*3 + move[0]), int(sub_game[1]*3 + move[1])] = self.player
        return move, sub_game
           
    def iterate_game(self):
        move, sub_game = self.make_move()
        #checks sub board thats just been played to see if it has been won or drawn
        sub_board = self.board[sub_game[0]*3:sub_game[0]*3+3, sub_game[1]*3:sub_game[1]*3+3]
        #updates meta board with with any new wins/draws
        board_win_state = self.check_game_won(sub_board)
        self.meta_board[sub_game[0],sub_game[1]] = board_win_state
        # if the subgame was drawn or won, set the next move to be a free one
        if board_win_state != 0:
            move = np.array([np.nan, np.nan])
            
        #checks if the total game has been won/drawn
        game_win_state = self.check_game_won(self.meta_board)
        if game_win_state == self.player:
            print("Player {} wins".format(player_str(self.player)))
            return False
        elif np.isnan(game_win_state) == True:
            print("Game is draw")
            game_sum = np.sum(self.meta_board)
            if game_sum > 0:
                print("Player X controls the board")
            elif game_sum < 0:
                print("Player O controls the board")
            else:
                print("No one controls the board")
            return False
        else:
           #iterate the player and last move
           self.player = -1*self.player
           self.last_move = move
           return True
       
    def iterate_ai(self, move, sub_game):
        self.board[int(sub_game[0]*3 + move[0]), int(sub_game[1]*3 + move[1])] = self.player

        #checks sub board thats just been played to see if it has been won or drawn
        sub_board = self.board[sub_game[0]*3:sub_game[0]*3+3, sub_game[1]*3:sub_game[1]*3+3]
        #updates meta board with with any new wins/draws
        board_win_state = self.check_game_won(sub_board)
        self.meta_board[sub_game[0],sub_game[1]] = board_win_state
        # if the subgame was drawn or won, set the next move to be a free one
        if board_win_state != 0:
            move = np.array([np.nan, np.nan])
            
        #checks if the total game has been won/drawn
        game_win_state = self.check_game_won(self.meta_board)
        if game_win_state == self.player:
            print("Player {} wins".format(player_str(self.player)))
            return False
        elif np.isnan(game_win_state) == True:
            print("Game is draw")
            game_sum = np.sum(self.meta_board)
            if game_sum > 0:
                print("Player X controls the board")
            elif game_sum < 0:
                print("Player O controls the board")
            else:
                print("No one controls the board")
            return False
        else:
           #iterate the player and last move
           self.player = -1*self.player
           self.last_move = move
           return True
       
    def iterate_rollout(self, move, sub_game):
    
        #checks sub board thats just been played to see if it has been won or drawn
        sub_board = self.board[sub_game[0]*3:sub_game[0]*3+3, sub_game[1]*3:sub_game[1]*3+3]
        #updates meta board with with any new wins/draws
        board_win_state = self.check_game_won(sub_board)
        self.meta_board[sub_game[0],sub_game[1]] = board_win_state
        # if the subgame was drawn or won, set the next move to be a free one
        if board_win_state != 0:
            move = np.array([np.nan, np.nan])
            
        #checks if the total game has been won/drawn
        game_win_state = self.check_game_won(self.meta_board)
        if game_win_state == self.player:
            return False, self.player
        elif np.isnan(game_win_state) == True:
            return False, 0
        else:
           #iterate the player and last move
           self.player = -1*self.player
           self.last_move = move
           return True, 0

def player_str(player):
    if player == 0:
        return " "
    elif player == 1:
        return "X"
    elif player == "-":

        return "-"
    
    else:
        return "O"
    
    
def drawboard(game):
    board = game.board
    
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
            elif np.isnan(game.meta_board[i//3,j//3]) == True:
                
                fill = "-"
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
            
        print(substring + "#")
        
    print("------------#-----------#------------")
    
