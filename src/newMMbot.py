# -*- coding: utf-8 -*-
"""
Minimax bot

Coding strategy:
  - Recursive method that goes through every possible move one after the other
  - Uses alpha-beta pruning to trim down the number of branches it actually has to traverse
"""

import cubicTTT
import math

# Alpha = maxes, Beta = mins
class MinimaxBot:
  
  def __init__(self, game, piece, oppPiece):
    #The game argument doesn't actually get used
    self.game = game
    self.piece = piece
    self.oppPiece = oppPiece
    self.MAX_VAL = 999
    self.MIN_VAL = -999
  
  
  class Node:
    # This is a node for the minimax tree structure
    
    # Moves are from 00000000000000000000000000 to 22222222222222222222222222
    # These represent 0 (no move), 1 (p1 move), 2 (p2 move) in each of the 26 
    # unique moves.
    
    # Move dictionary:
    # TOP-side 9 moves are the first 9 digits, with top left being the first 
    # digit, and bottom-right being the 9th digit.
    # BOT-side 9 moves are the next 9 digits, same as TOP-side
    # 19th digit is front-side center-row left cell
    # 20th digit is front middle (all of these are center-row, so I omit it)
    # 21st digit is front right
    # 22nd digit is back left
    # 23rd digit is back middle
    # 24th digit is back right
    # 25th digit is left middle
    # 26th digit is right middle
    
    
    # Setup fields and create a bunch of child nodes
    # If a leaf, set fields to indicate that and evaluate current position
    def __init__(self, Outer, currMove, moveID):
      self.children = []
      self.currMove = currMove
      self.moveID = self.applyMove(currMove, moveID)
      self.Outer = Outer
      self.pos = {  1 : ("top", 0),
                    2 : ("top", 1),
                    3 : ("top", 2),
                    4 : ("top", 3),
                    5 : ("top", 4),
                    6 : ("top", 5),
                    7 : ("top", 6),
                    8 : ("top", 7),
                    9 : ("top", 8),
                    10 : ("bottom", 0),
                    11 : ("bottom", 1),
                    12 : ("bottom", 2),
                    13 : ("bottom", 3),
                    14 : ("bottom", 4),
                    15 : ("bottom", 5),
                    16 : ("bottom", 6),
                    17 : ("bottom", 7),
                    18 : ("bottom", 8),
                    19 : ("front", 4),
                    20 : ("front", 5),
                    21 : ("front", 6),
                    22 : ("back", 4),
                    23 : ("back", 5),
                    24 : ("back", 6),
                    25 : ("left", 5),
                    26 : ("right", 5)}
      
      
      moveList = self.getMoves(moveID)
      
      if(len(moveList) != 0):
        for move in moveList:
          newMoveID = 0;
          child = MinimaxBot.Node(newMoveID)
          self.children.append(child)
      else:
        currGame = self.makeGame(self.moveID)
        self.value = self.heuristicAlg(currGame)
        self.leaf = True
    
    # Returns the best value along with the move used to get there
    def getValue(self):    
      if (self.leaf):
        return (self.value, self.currMove)
      else:
        maxVal = self.Outer.MAX_VAL
        for child in self.children:
          currVal = child.getValue()
          if(currVal > maxVal):
            maxVal = currVal
            bestMove = child.currMove
        return (maxVal, bestMove)
      
    # Gets all open moves for the current moveset
    def getMoves(self, moveID):
      moveList = []
      for i in range(1,27):
        # This gets the digit at position i
        thisMove = math.floor(moveID / pow(10, 26-i)) % 10
        
        if thisMove == 0:
          moveList.append(i)
      return moveList
    
    
    # Makes a blank game and applies the current moves to that game
    def makeGame(self, moveID):
      game = cubicTTT.CubicTicTacToe()
      
      for i in range(1,27):
        # This gets the digit at position i
        thisMove = math.floor(moveID / pow(10, 26-i)) % 10
        
        # 1 means 1st player's move
        if thisMove == 1:
          position = self.pos(i) # Side, cell pair
          game.make_move(game.first_player(), position[0], position[1])
        # 2 means 2nd player's move
        elif thisMove == 2:
          position = self.pos(i) # Side, cell pair
          game.make_move(game.second_player(), position[0], position[1])
        # 0 means no move, so I don't need to record it
        
      return game
    
    # Applies a move to the current moveset
    def applyMove(self, currMove, moveID):
      moveID = moveID + self.player * pow(10, 26 - (currMove))
      return moveID
    
    
    
    
      
      # TODO - Finish calculateTree to make the first node and start the process
      # - Add a depth argument and make it stop when it hits that depth
      #   This will require throwing away of useless data and applying a move to start
      # - Make the nodes return the (side, cell) instead of my int position
      # - Add self.player argument and have it alternate so the nodes know which
      #   player they are
      # - Add alpha-beta pruning when evaluating
      # - Test if working
      # - Add duplicate checking
      
      
      
    
      
  

    
  # Make the tree structure
  def calculateTree(self):
    self.tree = MinimaxBot.Node(self, -1, 0)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  #This works like the maxAlg, but needs a different return
  def getNextMove(self, currGame, depth):
    moveList = currGame.availableMoves()
    
    if len(moveList) == 0 or depth < 1:
      #Not sure how to handle this case
      return -1
    
    alpha = self.MIN_VAL
    beta = self.MAX_VAL
    for move in moveList:
      temp = currGame.copy()
      temp.nextMove(move, self.piece)
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
      if(len(currGame.availableMoves()) == 0):
        return self.heuristicAlg(currGame)
      #Go through every move, copy the game, apply a move, call the min part.
      for move in currGame.availableMoves():
        temp = currGame.copy()
        temp.nextMove(move, self.piece)
        value = self.miniAlg(temp, depth-1, alpha, beta)
        if(value > alpha):
          alpha = value
        if(alpha > beta):
          break
      return value
  
  def miniAlg(self, currGame, depth, alpha, beta):
    #Check if we are at the depth limit, if so, return heuristic
    if(depth == 1):
      return self.heuristicAlg(currGame)
    else:
      #Check if there are more moves, if not, return heuristic
      if(len(currGame.availableMoves()) == 0):
        return self.heuristicAlg(currGame)
      #Go through every move, copy the game, apply a move, call the max part.
      for move in currGame.availableMoves():
        temp = currGame.copy()
        temp.nextMove(move, self.oppPiece)
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