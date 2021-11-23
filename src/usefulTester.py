# -*- coding: utf-8 -*-
"""
Tests minimaxbot
"""

import cubicTTT as cT
import minimaxbot as mM
import time as tI


start_time = tI.perf_counter_ns()

game = cT.CubicTicTacToe()

## Here are some sample moves to get the game started 
# (the X moves were decided by a depth=4 bot)
# game.make_move('X', "top", 0)
# game.make_move('O', "right", 5)
# game.make_move('X', "left", 6)
# game.make_move('O', "bottom", 3)
# game.make_move('X', "top", 1)
# game.make_move('O', "bottom", 4)
# game.make_move('X', "top", 4)
# game.make_move('O', "right", 4)

end_time_1 = tI.perf_counter_ns()
print(f"Play Moves Time: {end_time_1 - start_time}")



# This means create a minimax bot with move X, against move O, that is player
# 1, and uses heuristic alg 1 (the new one, the old one is any other integer)
bot = mM.MinimaxBot('X', 'O', 1, 1)

# Depth = 4 means 3 moves, as the depth refers to how many levels of the tree
# there are and each move passes between levels
(side, spot) = bot.calculateTree(game, 4)
game.make_move('X', side, spot)

# Print out the bot's move to see what it chose
print(f'Bots move: {side}, {spot}')

# This is 'your' move
game.make_move('O', "left", 4)

print(f'Number of prunings: {bot.count}')

end_time_2= tI.perf_counter_ns()
print(f"Calculate Tree Time (ns): {end_time_2 - end_time_1}")

game.display_game()
print(f'X-score: {game.x_score}, O-score: {game.o_score}')







