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

#game.make_move('O', "bottom", 4)

##### Takes about 3 minutes, 18 seconds to do the above (198 seconds)

#game.make_move('O', "back", 4)

##### Takes about 18 seconds to do the above

#game.make_move('X', "front", 3)

##### Takes maybe 3 seconds to do the above

#game.make_move('O', "front", 5)

##### Literally instant to do the above 

#game.make_move('O', "back", 3)
#game.make_move('O', "back", 5)

#game.make_move('X', "top", 5)
#game.make_move('O', "bottom", 3)

## remove these later

#game.make_move('X', "top", 3)
#game.make_move('O', "bottom", 5)

end_time_1 = tI.perf_counter_ns()
print(f"Play Moves Time: {end_time_1 - start_time}")

print(game.open_unique_moves())

bot = mM.MinimaxBot(game, 'X', 'O', 1)
bot.calculateTree(game)

end_time_2= tI.perf_counter_ns()
print(f"Calculate Tree Time: {end_time_2 - end_time_1}")

print(bot.evalPosition(game))

end_time_3 = tI.perf_counter_ns()
print(f"Eval Position Time: {end_time_3 - end_time_2}")






