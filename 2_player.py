# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 18:13:06 2020

@author: Robin
"""
import numpy as np
from main import game, drawboard
# game loop
game = game()
drawboard(game)
game.meta_board[0,0] = np.nan
game_cont  = True
while game_cont == True:
    
    game_cont = game.iterate_game()
    drawboard(game)