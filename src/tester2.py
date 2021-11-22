# -*- coding: utf-8 -*-
"""
Tests minimaxbot
"""

import cubicTTT as cT
import minimaxbot as mM
import time as tI


start_time = tI.perf_counter_ns()

game = cT.CubicTicTacToe()


end_time_1 = tI.perf_counter_ns()
print(f"Play Moves Time: {end_time_1 - start_time}")



# This means create a minimax bot with move X, against move O, that is player
# 1, and uses heuristic alg 1 (the new one, the old one is any other integer)
bot = mM.MinimaxBot('X', 'O', 1, 1)

(side, spot) = bot.calculateTree(game, 3)
game.make_move('X', side, spot)


game.make_move('O', "bottom", 4)

(side, spot) = bot.calculateTree(game, 3)
game.make_move('X', side, spot)

# game.make_move('O', "top", 1)

# (side, spot) = bot.calculateTree(game, 2)
# game.make_move('X', side, spot)

# game.make_move('O', "top", 3)

# (side, spot) = bot.calculateTree(game, 2)
# game.make_move('X', side, spot)

# game.make_move('O', "left", 4)

# (side, spot) = bot.calculateTree(game, 3)
# game.make_move('X', side, spot)

# Takes .2 sec for depth = 3 (2 moves)
# Takes 4.4 sec for depth = 4 (3 moves) (Getting like 4.9 to 5s now)
# Takes 112 sec for depth = 5 (4 moves)
# These almost exactly show the *20 performance effect of adding another level

print(game.open_unique_moves())

# It looks like a little bit of time is being added because of the maintaining
# of ID, lets see if we save time overall when using it to remove duplicates
# pre-duplicate checking: like 5.3s for depth = 4)


end_time_2= tI.perf_counter_ns()
print(f"Calculate Tree Time: {end_time_2 - end_time_1}")

game.display_game()
print(game.x_score)
print(game.o_score)

for child in bot.root.children:
  print(child.currMove, child.alpha, child.beta)







