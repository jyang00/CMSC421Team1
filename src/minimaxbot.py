# -*- coding: utf-8 -*-
"""
Minimax bot

Coding strategy:
  - Recursive method that goes through every possible move one after the other
  - IDK how to do the alpha-beta pruning, we can get back to that later

"""


class MinimaxBot:
  
  def __init(self, game, piece):
    self.game = game
    self.piece = piece
    
  def getNextMove(self, currGame, depth):
    moveList = currGame.availableMoves()
    values = []
    for move in moveList:
      temp = currGame.copy()
      temp.nextMove(move, self.piece)
      values.append(self.minimaxAlg(temp, depth-1))
    bestMove = moveList[values.index(max(values))]
    return bestMove
  
  def minimaxAlg(self, currGame, depth):
    if(depth == 1):
      return self.heuristicAlg(currGame)
    else:
      if(len(currGame.availableMoves()) == 0):
        return self.heuristicAlg(currGame)
      values = []
      for move in currGame.availableMoves():
        temp = currGame.copy()
        temp.nextMove(move, self.piece)
        values.append(self.minimaxAlg(temp, depth-1))
      return max(values)
    
  def heuristicAlg(self, currGame):
    # Currently left blank, but make sure it returns a massive value on game 
    # win, a negative massive value on game loss, and everything in between
    return 0