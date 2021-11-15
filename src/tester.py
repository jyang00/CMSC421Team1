# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 15:58:54 2021

@author: acneu
"""

import cubicTTT as cT
import newMMbot as mM
import time as tI


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

game.make_move('X', "front", 4)
game.make_move('X', "top", 4)
game.make_move('O', "bottom", 4)

game.make_move('O', "back", 4)
game.make_move('X', "front", 3)
game.make_move('X', "front", 5)


########## Temp moves
game.make_move('X', "bottom", 5)
game.make_move('O', "top", 3)



##########






#game.make_move('O', "back", 3)
#game.make_move('O', "back", 5)
#game.make_move('X', "top", 5)

#game.make_move('O', "bottom", 3)
#game.make_move('X', "top", 3)
#game.make_move('O', "bottom", 5)

#game.make_move('X', "left", 4)
#game.make_move('O', "right", 4)



end_time_1 = tI.perf_counter_ns()
print(f"Play Moves Time: {end_time_1 - start_time}")

print(game.open_unique_moves())

bot = mM.MinimaxBot('X', 'O', 1, 1)
print(bot.calculateTree(game, 3))
print(f"Keys in table: {len(bot.nodeTable.keys())}")
print(f"Current moves played: {len(game.x_moves) + len(game.o_moves)}")

## Currently seeing around 15 seconds for depth 5, scaling down to 6.5 seconds
## around 8 moves in, scaling down to 2.5 seconds around 12 moves in, down to
## 0.63 seconds around 16 moves in, down to 0.005 seconds around 22 moves in

## 10 seconds for 6 moves in, 13 seconds for 4 moves in

## Basically looks like logarithmic or inverse square

## This is without the heuristic function plugged in, so I expect it to take
## much longer with it in


end_time_2= tI.perf_counter_ns()
print(f"Calculate Tree Time: {end_time_2 - end_time_1}")

#print(bot.evalPosition(game))

#end_time_3 = tI.perf_counter_ns()
#print(f"Eval Position Time: {end_time_3 - end_time_2}")

game.display_game()
print(game.x_score)
print(game.o_score)






