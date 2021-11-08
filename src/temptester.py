# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 20:42:09 2021

@author: acneu
"""

import cubicTTT as cT
import time as tI
import minimaxbot as oB


start_time = tI.perf_counter_ns()

game = cT.CubicTicTacToe()

game.make_move('X', "top", 0)
game.make_move('X', "top", 1)
game.make_move('X', "top", 2)

game.make_move('O', "bottom", 0)
game.make_move('O', "bottom", 1)
game.make_move('O', "bottom", 2)

game.make_move('X', "top", 6)
game.make_move('X', "top", 7)
game.make_move('X', "top", 8)

game.make_move('O', "bottom", 6)
game.make_move('O', "bottom", 7)
game.make_move('O', "bottom", 8)

#game.make_move('X', "front", 4)
#game.make_move('X', "top", 4)
#game.make_move('O', "bottom", 4)

#game.make_move('O', "back", 4)
game.make_move('X', "front", 3)
game.make_move('X', "front", 5)


game.make_move('O', "back", 3)
game.make_move('O', "back", 5)
#game.make_move('X', "top", 5)

#game.make_move('O', "bottom", 3)
#game.make_move('X', "top", 3)
#game.make_move('O', "bottom", 5)

#game.make_move('X', "left", 4)
#game.make_move('O', "right", 4)

#### 16 moves in, takes about 9.5 seconds for depth 5

end_time_1 = tI.perf_counter_ns()
print(f"Play Moves Time: {end_time_1 - start_time}")

print(game.open_unique_moves())

bot = oB.MinimaxBot(game, 1, game.first_player(), game.second_player())
bot.getNextMove(game, 5)

end_time_2= tI.perf_counter_ns()
print(f"Calculate Tree Time: {end_time_2 - end_time_1}")








