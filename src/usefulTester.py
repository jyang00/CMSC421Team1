# -*- coding: utf-8 -*-
"""
Tests minimaxbot
"""

import cubicTTT as cT
import minimaxbot as mM
import time as tI
import tracemalloc as tM

start_time = tI.process_time_ns()

game = cT.CubicTicTacToe()

## Game 1 - Tie (I tried for BEST moves, depth 4)
# game.make_move('X', "top", 0)
# game.make_move('O', "top", 2)
# game.make_move('X', "top", 8)
# game.make_move('O', "right", 6)
# game.make_move('X', "top", 6)
# game.make_move('O', "right", 8)
# game.make_move('X', "top", 3)
# game.make_move('O', "right", 7)
# game.make_move('X', "back", 3)
# game.make_move('O', "front", 1)
# game.make_move('X', "bottom", 0)
# game.make_move('O', "back", 8)
# game.make_move('X', "top", 1)
# game.make_move('O', "front", 3)
# game.make_move('X', "front", 4)
# game.make_move('O', "back", 7)


## Game 2 - Bot Win (I tried for immediate side wins, depth 4)
# game.make_move('X', "top", 0)
# game.make_move('O', "top", 8)
# game.make_move('X', "bottom", 0)
# game.make_move('O', "left", 4)
# game.make_move('X', "top", 6)
# game.make_move('O', "left", 5)
# game.make_move('X', "top", 3)
# game.make_move('O', "right", 8)
# game.make_move('X', "bottom", 2)
# game.make_move('O', "bottom", 1)
# game.make_move('X', "right", 4)
# game.make_move('O', "right", 2)
# game.make_move('X', "back", 3)
# game.make_move('O', "right", 1)
# game.make_move('X', "front", 4)
# game.make_move('O', "bottom", 7)
# game.make_move('X', "bottom", 6)
# game.make_move('O', "bottom", 4)

## Game 3 - Bot Win (bot was 2nd player = O. I tried for smart moves after 
## making a random first move, I got completely blown out. I probably didn't 
## look hard enough for smart moves though.)
# game.make_move('X', "back", 3)
# game.make_move('O', "top", 0)
# game.make_move('X', "top", 8)
# game.make_move('O', "bottom", 0)
# game.make_move('X', "bottom", 8)
# game.make_move('O', "top", 2)
# game.make_move('X', "top", 1)
# game.make_move('O', "bottom", 2)
# game.make_move('X', "bottom", 1)
# game.make_move('O', "right", 4)
# game.make_move('X', "top", 7)
# game.make_move('O', "top", 6)
# game.make_move('X', "front", 4)
# game.make_move('O', "top", 3)
# game.make_move('X', "bottom", 7)
# game.make_move('O', "bottom", 6)
# game.make_move('X', "back", 4)


end_time_1 = tI.process_time_ns()
print(f"Play Moves Time: {end_time_1 - start_time}")


# This means create a minimax bot with move X, against move O, that is player
# 1, and uses heuristic alg 1 (the new one, the old one is any other integer)
bot = mM.MinimaxBot('X', 'O', 1, 1)

## Below line is used when bot is second player
# bot = mM.MinimaxBot('O', 'X', 2, 1)

# Depth = 4 means 3 moves, as the depth refers to how many levels of the tree
# there are and each move passes between levels
# tM.start()
(side, spot) = bot.calculateTree(game, 4)
# current, peak = tM.get_traced_memory()
# print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
# tM.stop()
game.make_move('X', side, spot)

## Below line is used when bot is second player
#game.make_move('O', side, spot)

# Print out the bot's move to see what it chose
print(f'Bots move: {side}, {spot}')








print(f'Number of prunings: {bot.count}')

end_time_2= tI.process_time_ns()
print(f"Calculate Tree Time (sec): {(end_time_2 - end_time_1)/1000000000}")

game.display_game()
print(f'X-score: {game.x_score}, O-score: {game.o_score}')
print(f'Heuristic Time (sec): {bot.time1/1000000000}, Copy Time (sec): {bot.time2/1000000000}')
print(f'Make Move Time (sec): {bot.time3/1000000000}')
print(f'Get Movelist Time (sec): {bot.time4/1000000000}')
#print(f'Game Times ---- Time 1 (sec): {bot.time4/1000000000}, Time 2 (sec): {bot.time5/1000000000}')
## Depth 5 starts out around 45s, but drops to like 6 seconds 8 moves in, so I think we can use it

## Depth 6 gets down to like 50s 12 moves in, so we should really only use it
## like halfway into the game. It drops to 20ish seconds (large variation) 2 moves later (14 total)
## It drops to 8s 16 moves in
## It drops to 2s 18 moves in

## Depth 7 gets to 8 seconds 18 moves in, 15s 17 moves in, 37s 16 moves in



