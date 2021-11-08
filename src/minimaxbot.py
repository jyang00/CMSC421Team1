# -*- coding: utf-8 -*-
"""
Minimax bot

Coding strategy:
  - Recursive method that goes through every possible move one after the other
  - Uses alpha-beta pruning to trim down the number of branches it actually has to traverse
"""


# Alpha = maxes, Beta = mins
class MinimaxBot:
  
  
  def __init__(self, game, player, piece, oppPiece):
    #This doesn't actually get used
    self.game = game
    self.player = player
    self.piece = piece
    self.oppPiece = oppPiece
    self.MAX_VAL = 999
    self.MIN_VAL = -999
    
  #This works like the maxAlg, but needs a different return
  def getNextMove(self, currGame, depth):
    moveList = currGame.open_unique_moves()
    
    if len(moveList) == 0 or depth < 1:
      #Not sure how to handle this case
      return -1
    
    alpha = self.MIN_VAL
    beta = self.MAX_VAL
    for move in moveList:
      temp = currGame.copy()
      temp.make_move(self.piece, move[0], move[1])
      value = self.miniAlg(temp, depth-1, alpha, beta)
      if(value > alpha):
        alpha = value
        bestMove = move
    return bestMove
  
  def maxAlg(self, currGame, depth, alpha, beta):
    #Check if we are at the depth limit, if so, return heuristic
    if(depth == 0):
      return self.heuristicAlg(currGame)
    else:
      #Check if there are more moves, if not, return heuristic
      moveList = currGame.open_unique_moves()
      if(len(moveList) == 0):
        return self.heuristicAlg(currGame)
      #Go through every move, copy the game, apply a move, call the min part.
      for move in moveList:
        temp = currGame.copy()
        temp.make_move(self.piece, move[0], move[1])
        value = self.miniAlg(temp, depth-1, alpha, beta)
        if(value > alpha):
          alpha = value
        if(alpha > beta):
          break
      return value
  
  def miniAlg(self, currGame, depth, alpha, beta):
    #Check if we are at the depth limit, if so, return heuristic
    if(depth == 0):
      return self.heuristicAlg(currGame)
    else:
      #Check if there are more moves, if not, return heuristic
      moveList = currGame.open_unique_moves()
      if(len(moveList) == 0):
        return self.heuristicAlg(currGame)
      #Go through every move, copy the game, apply a move, call the max part.
      for move in moveList:
        temp = currGame.copy()
        temp.make_move(self.oppPiece, move[0], move[1])
        value = self.maxAlg(temp, depth-1, alpha, beta)
        if(value < beta):
          beta = value
        if(beta < alpha):
          break
      return value
  
  def heuristicAlg(self, currGame):
    # Currently left blank, but make sure it returns a massive value on game 
    # win, a negative massive value on game loss, and everything in between
    return 0