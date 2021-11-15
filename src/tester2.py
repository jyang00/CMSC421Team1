# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 20:33:18 2021

@author: acneu
"""

import cubicTTT as cT
import tempMMbot as mM
import time as tI


start_time = tI.perf_counter_ns()

game = cT.CubicTicTacToe()


end_time_1 = tI.perf_counter_ns()
print(f"Play Moves Time: {end_time_1 - start_time}")



# This means create a minimax bot with move X, against move O, that is player
# 1, and uses heuristic alg 1 (the new one, the old one is any other integer)
bot = mM.MinimaxBot('X', 'O', 1, 1)
print(bot.calculateTree(game, 2))

(side, spot) = bot.calculateTree(game, 2)
game.make_move('X', side, spot)

game.make_move('O', "bottom", 4)

(side, spot) = bot.calculateTree(game, 2)
game.make_move('X', side, spot)

game.make_move('O', "top", 1)

(side, spot) = bot.calculateTree(game, 2)
game.make_move('X', side, spot)

game.make_move('O', "top", 3)

(side, spot) = bot.calculateTree(game, 2)
game.make_move('X', side, spot)

game.make_move('O', "left", 4)

(side, spot) = bot.calculateTree(game, 3)
game.make_move('X', side, spot)



print(game.open_unique_moves())



end_time_2= tI.perf_counter_ns()
print(f"Calculate Tree Time: {end_time_2 - end_time_1}")


game.display_game()
print(game.x_score)
print(game.o_score)






