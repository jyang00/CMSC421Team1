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
  
  def __init__(self, game, piece, oppPiece, player):
    #The game argument doesn't actually get used
    self.game = game
    self.piece = piece
    self.oppPiece = oppPiece
    self.MAX_VAL = 999
    self.MIN_VAL = -999
    self.nodeTable = {}
    self.player = player
  
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
    def __init__(self, Outer, currMove, moveID, alpha, beta, isMax, player):
      self.children = []
      #currMove is an integer from 1 to 26, representing which digit we're on (left to right)
      self.currMove = currMove
      self.moveID = moveID #Right now, the parent passes the moveID with the move already applied
      #self.moveID = self.applyMove(currMove, moveID)
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
      self.alpha = alpha
      self.beta = beta
      self.isMax = isMax
      self.player = player
      
      moveList = self.getMoves(moveID)
      if(len(moveList) != 0):
        #Try every move
        for move in moveList:
          newMoveID = self.applyMove(move, self.moveID)
          #Check table for duplicate
          if not(self.Outer.nodeTable.has_key(newMoveID)):
            child = MinimaxBot.Node(Outer, move, self.moveID, self.alpha, self.beta, (1 + self.isMax) % 2, (self.player)%2 + 1)
            self.children.append(child)
            self.Outer.nodeTable[newMoveID] = child
          #If duplicate, add a link from this node to that child
          else:
            self.children.append(self.Outer.nodeTable[newMoveID])
      #This means no children, so must be a leaf node
      else:
        currGame = self.makeGame(self.moveID)
        self.value = self.heuristicAlg(currGame)
        self.leaf = True
      
      if isMax:
        self.alpha = self.getValue()
      else:
        self.beta = self.getValue()
    
    
    # Returns the best value along with the move used to get there
    def getValue(self):    
      if (self.leaf):
        return (self.value, self.currMove)
      else:
        #If max node, use alpha + maxes
        if self.isMax:
          maxVal = self.alpha
          for child in self.children:
            currVal = child.getValue()
            if(currVal > maxVal):
              maxVal = currVal
              bestMove = child.currMove
          return (maxVal, bestMove)
        #If min node, use beta + mins
        else:
          minVal = self.beta
          for child in self.children:
            currVal = child.getValue()
            if(currVal < minVal):
              minVal = currVal
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
      # (Just need to use my translator table that takes 1 to 26 and outputs (side, cell))
      # - Add alpha-beta pruning when evaluating
      # - Test if working
      # - Add duplicate checking
      
      # PARTIAL TODO - Continue with calculateTree so I can start testing stuff
      # and handle partially completed games
      # - Work with getValue to make sure it is returning something usable
      # - Work with the nodes to allow calculateTree (or another method) to use
      # already available results
      # - Return a move to play from the methods
      
    
      
  

    
  # Make the tree structure
  def calculateTree(self, currGame):
    #currMove = -1 means it is the first node and there isn't a move yet
    moveID = self.convertGame(currGame)
    self.root = MinimaxBot.Node(self, -1, moveID, self.MIN_VAL, self.MAX_VAL, 1, self.player)
    self.root.getValue()
    
  def evalPosition(self, currGame):
    moveID = self.convertGame(currGame)
    currNode = self.nodeTable[moveID]
    return currNode.getValue()
    
  #Convert the game from a board to my integer format
  def convertGame(self, currGame):
    moveID = 0
    cube = currGame.cube
    #Handle the top face
    for i in range(1,10):
      currPiece = cube["top"][i - 1]
      #Check which piece is in this position
      if currPiece == self.piece:
        moveID = moveID + self.player * pow(10, 26 - i)
      elif currPiece == self.oppPiece:
        moveID = moveID + ((self.player % 2) + 1) * pow(10, 26 - i)
        
    #Handle the bottom face
    for i in range(1,10):
      currPiece = cube["bottom"][i - 1]
      #Check which piece is in this position
      if currPiece == self.piece:
        moveID = moveID + self.player * pow(10, 26 - 9 - i)
      elif currPiece == self.oppPiece:
        moveID = moveID + ((self.player % 2) + 1) * pow(10, 26 - 9 - i)
    
    #Handle the front face
    for i in range(4,7):
      currPiece = cube["front"][i - 1]
      #Check which piece is in this position
      if currPiece == self.piece:
        moveID = moveID + self.player * pow(10, 26 - 18 - i)
      elif currPiece == self.oppPiece:
        moveID = moveID + ((self.player % 2) + 1) * pow(10, 26 - 18 - i)
    
    #Handle the back face
    for i in range(4,7):
      currPiece = cube["back"][i - 1]
      #Check which piece is in this position
      if currPiece == self.piece:
        moveID = moveID + self.player * pow(10, 26 - 21 - i)
      elif currPiece == self.oppPiece:
        moveID = moveID + ((self.player % 2) + 1) * pow(10, 26 - 21 - i)
    
    #Handle left middle
    currPiece = cube["left"][4]
    if currPiece == self.piece:
      moveID = moveID + self.player * pow(10, 1)
    elif currPiece == self.oppPiece:
      moveID = moveID + ((self.player % 2) + 1) * pow(10, 1)
      
    #Handle right middle
    currPiece = cube["right"][4]
    if currPiece == self.piece:
      moveID = moveID + self.player * pow(10, 0)
    elif currPiece == self.oppPiece:
      moveID = moveID + ((self.player % 2) + 1) * pow(10, 0)
    
    return moveID
    
    
    
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