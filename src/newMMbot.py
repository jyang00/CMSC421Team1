# -*- coding: utf-8 -*-
"""
Minimax bot

Coding strategy:
  - Recursive method that goes through every possible move one after the other
  - Uses alpha-beta pruning to trim down the number of branches it actually has to traverse
"""

import cubicTTT

# Alpha = maxes, Beta = mins
class MinimaxBot:
  
  def __init__(self, piece, oppPiece, player, heurAlg):
    # The game argument doesn't actually get used
    self.piece = piece
    self.oppPiece = oppPiece
    self.MAX_VAL = 999
    self.MIN_VAL = -999
    self.nodeTable = {}
    self.player = player
    self.convTable = {"X" : 1,
                      "O" : 3,
                      "-" : 0}
    self.heurisTable = { 0 : 0,
                         1 : 1,
                         2 : 2,
                         3 : -1,
                         4 : 0,
                         5 : 0,
                         6 : -2,
                         7 : 0}
    # heurAlg should either be 1 for the new alg, or anything else for the old alg
    self.heurAlg = heurAlg
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
    def __init__(self, Outer, currMove, moveID, alpha, beta, isMax, player, depth):
      self.children = []
      # currMove is an integer from 1 to 26, representing which digit we're on 
      # (left to right, so 1 is the far left digit)
      self.currMove = currMove
      # moveID is a 26-digit integer of the current game state with the current
      # move already applied
      self.moveID = moveID 
      # Outer is a link to the MinimaxBot object so it can use certain fields
      self.Outer = Outer
      # pos is a dict mapping of currMove numbers to actual moves
      self.pos = {  -1: ("", -1),
                    1 : ("top", 0),
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
                    19 : ("front", 3),
                    20 : ("front", 4),
                    21 : ("front", 5),
                    22 : ("back", 3),
                    23 : ("back", 4),
                    24 : ("back", 5),
                    25 : ("left", 4),
                    26 : ("right", 4)}
      self.alpha = alpha
      self.beta = beta
      self.isMax = isMax
      self.player = player
      # When incoming depth is 1, we stop
      self.depth = depth
      # Leaf is an indicator to the algorithm that this is the end of the tree
      # with leaf, we know when to start calculating heuristics
      self.leaf = False
      
      moveList = self.getMoves(self.moveID)
      if(len(moveList) != 0 and depth > 1):
        # Try every move
        for move in moveList:
          newMoveID = self.applyMove(move, self.moveID)
          # Check table for duplicate
          if newMoveID not in self.Outer.nodeTable:
            # Make a new child with the new move and ID, with opposite isMax 
            # and player, and decremented depth
            child = MinimaxBot.Node(self.Outer, move, newMoveID, self.alpha, self.beta, (1 + self.isMax) % 2, (self.player)%2 + 1, depth - 1)
            self.children.append(child)
            self.Outer.nodeTable[newMoveID] = child
          # If duplicate, add a link from this node to that child
          else:
            # Two gamestates being identical through different paths can only
            # occur at the same level, so I don't need to worry about keeping
            # track of different depth levels.
            self.children.append(self.Outer.nodeTable[newMoveID])
      # This means no children, so must be a leaf node
      else:
        currGame = self.makeGame(self.moveID)
        if self.Outer.heurAlg == 1:
          self.value = self.Outer.newheuristicAlg(currGame)
        else:
          self.value = self.Outer.oldheuristicAlg(currGame)
        self.leaf = True
      
      if self.isMax:
        self.alpha = self.getValue()[0]
      else:
        self.beta = self.getValue()[0]
    
    
    # Returns the best value along with the move used to get there
    def getValue(self):    
      if (self.leaf):
        return (self.value, self.currMove)
      else:
        # If max node, use alpha + maxes
        if self.isMax:
          maxVal = self.Outer.MIN_VAL
          for child in self.children:
            result = (child.beta, child.currMove)
            currVal = result[0]
            if(currVal > maxVal):
              maxVal = currVal
              bestMove = result[1]
          return (maxVal, bestMove)
        # If min node, use beta + mins
        else:
          minVal = self.Outer.MAX_VAL
          for child in self.children:
            result = (child.alpha, child.currMove)
            currVal = result[0]
            if(currVal < minVal):
              minVal = currVal
              bestMove = result[1]
          return (minVal, bestMove)
      
      
    # Gets all open moves for the current moveset
    def getMoves(self, moveID):
      moveList = []
      for i in range(1,27):
        # This gets the digit at position i
        thisMove = (moveID // pow(10, 26 - i)) % 10
        if thisMove == 0:
          moveList.append(i)
      return moveList
    
    
    # Makes a blank game and applies the current moves to that game
    def makeGame(self, moveID):
      game = cubicTTT.CubicTicTacToe()
      
      for i in range(1,27):
        # This gets the digit at position i
        thisMove = (moveID // pow(10, 26 - i)) % 10
        # 1 means 1st player's move
        if thisMove == 1:
          position = self.pos[i] # Side, cell pair
          game.make_move(game.first_player(), position[0], position[1])
        # 2 means 2nd player's move
        elif thisMove == 2:
          position = self.pos[i] # Side, cell pair
          game.make_move(game.second_player(), position[0], position[1])
        # 0 means no move, so I don't need to record it    
      return game
    
    
    # Applies a move to the current moveset
    def applyMove(self, currMove, moveID):
      moveID = moveID + self.player * pow(10, 26 - (currMove))
      return moveID
    
    # Updates the nodes with the new depth and adds new layer/s onto them
    def updateNodes(self, depth):
      # Add self to hashmap if not already in it
      # This logic prevents duplicate states from redoing the same stuff
      if self.moveID not in self.Outer.nodeTable:
        self.Outer.nodeTable[self.moveID] = self
        self.depth = depth
        
        # If node is a leaf, add children (if possible)
        if self.leaf:
          self.leaf = False
          moveList = self.getMoves(self.moveID)
          if(len(moveList) != 0 and depth > 1):
            # Try every move
            for move in moveList:
              newMoveID = self.applyMove(move, self.moveID)
              # Check table for duplicate
              if newMoveID not in self.Outer.nodeTable:
                # Make a new child with the new move and ID, with opposite isMax 
                # and player, and decremented depth
                child = MinimaxBot.Node(self.Outer, move, newMoveID, self.alpha, self.beta, (1 + self.isMax) % 2, (self.player)%2 + 1, depth - 1)
                self.children.append(child)
                self.Outer.nodeTable[newMoveID] = child
              # If duplicate, add a link from this node to that child
              else:
                # Two gamestates being identical through different paths can only
                # occur at the same level, so I don't need to worry about keeping
                # track of different depth levels.
                self.children.append(self.Outer.nodeTable[newMoveID])
          # This means no children, so must be a leaf node
          else:
            currGame = self.makeGame(self.moveID)
            if self.Outer.heurAlg == 1:
              self.value = self.Outer.newheuristicAlg(currGame)
            else:
              self.value = self.Outer.oldheuristicAlg(currGame)
            self.leaf = True
        # If node is not a leaf, apply updateNodes to all of its children
        else:
          for child in self.children:
            child.updateNodes(depth - 1)
        
        # Update alpha/beta values because we have new levels added
        if self.isMax:
          self.alpha = self.getValue()[0]
        else:
          self.beta = self.getValue()[0]
    
     
      # TODO
      # - Add alpha-beta pruning when evaluating
      # - Make alg stop early if the game is over (don't need to try all moves)
      # - Combine calculateTree and evalPosition
      
     

    
  # Make the tree structure
  def calculateTree(self, currGame, depth):
    # currMove being -1 means it is the first node and there isn't a move yet
    moveID = self.convertGame(currGame)
    
    if moveID not in self.nodeTable:  
      self.root = MinimaxBot.Node(self, -1, moveID, self.MIN_VAL, self.MAX_VAL, 1, self.player, depth)
      self.nodeTable[moveID] = self.root
    else:
      # Get the root of the subtree that holds the current gamestate
      self.root = self.nodeTable[moveID]
      # Erase the hashmap of the tree to get rid of now-useless data
      self.nodeTable = {}
      # Update node values, add new levels, and add the useful data back to 
      #the hashmap
      self.root.updateNodes(depth)
      
    return self.root.pos[self.root.getValue()[1]]
    
    
  # Convert the game from a board to my integer format
  def convertGame(self, currGame):
    moveID = 0
    cube = currGame.cube
    # Handle the top face
    for i in range(0,9):
      currPiece = cube["top"][i]
      # Check which piece is in this position
      if currPiece == self.piece:
        moveID = moveID + self.player * pow(10, 26 - (i + 1))
      elif currPiece == self.oppPiece:
        moveID = moveID + ((self.player % 2) + 1) * pow(10, 26 - (i + 1))
    # Handle the bottom face
    for i in range(0,9):
      currPiece = cube["bottom"][i]
      # Check which piece is in this position
      if currPiece == self.piece:
        moveID = moveID + self.player * pow(10, 26 - 9 - (i + 1))
      elif currPiece == self.oppPiece:
        moveID = moveID + ((self.player % 2) + 1) * pow(10, 26 - 9 - (i + 1))
    # Handle the front face
    for i in range(3,6):
      currPiece = cube["front"][i]
      j = i - 3
      # Check which piece is in this position
      if currPiece == self.piece:
        moveID = moveID + self.player * pow(10, 26 - 18 - (j + 1))
      elif currPiece == self.oppPiece:
        moveID = moveID + ((self.player % 2) + 1) * pow(10, 26 - 18 - (j + 1))
    # Handle the back face
    for i in range(3,6):
      currPiece = cube["back"][i]
      j = i - 3
      # Check which piece is in this position
      if currPiece == self.piece:
        moveID = moveID + self.player * pow(10, 26 - 21 - (j + 1))
      elif currPiece == self.oppPiece:
        moveID = moveID + ((self.player % 2) + 1) * pow(10, 26 - 21 - (j + 1))
    # Handle left middle
    currPiece = cube["left"][4]
    if currPiece == self.piece:
      moveID = moveID + self.player * pow(10, 1)
    elif currPiece == self.oppPiece:
      moveID = moveID + ((self.player % 2) + 1) * pow(10, 1)
    # Handle right middle
    currPiece = cube["right"][4]
    if currPiece == self.piece:
      moveID = moveID + self.player * pow(10, 0)
    elif currPiece == self.oppPiece:
      moveID = moveID + ((self.player % 2) + 1) * pow(10, 0)
    return moveID
    
  def oldheuristicAlg(self, currGame):
    total = 0
    # Calculate # of wins, negate it if game is player2
    total += 50 * (currGame.x_score - currGame.o_score) * pow(-1, (self.player + 1 % 2))
    return total
  
  def newheuristicAlg(self, currGame):
    total = 0
    
    
    # Calculate # of wins
    total += 50 * (currGame.x_score - currGame.o_score)
    
    # Calculate # of 2 in a row and # of 1 in a row
    for side in currGame.winnable_sides:
      board = currGame.cube[side]
      
      # These equations convert X's to 1's, O's to 3's, and -'s to 0's.
      # This allows me to add up a row/column/diagonal and use the unique sums
      # to figure out what to add.
      # Ex. X - X = 2, which converts to adding 2 (or subtracting if max is O)
      
      # Calculate rows
      total += (self.heurisTable[self.convTable[board[0]] + self.convTable[board[1]] + self.convTable[board[2]]])
      total += (self.heurisTable[self.convTable[board[3]] + self.convTable[board[4]] + self.convTable[board[5]]])
      total += (self.heurisTable[self.convTable[board[6]] + self.convTable[board[7]] + self.convTable[board[8]]])
      # Calculate columns
      total += (self.heurisTable[self.convTable[board[0]] + self.convTable[board[3]] + self.convTable[board[6]]])
      total += (self.heurisTable[self.convTable[board[1]] + self.convTable[board[4]] + self.convTable[board[7]]])
      total += (self.heurisTable[self.convTable[board[2]] + self.convTable[board[5]] + self.convTable[board[8]]])
      # Calculate diagonals
      total += (self.heurisTable[self.convTable[board[0]] + self.convTable[board[4]] + self.convTable[board[8]]])
      total += (self.heurisTable[self.convTable[board[2]] + self.convTable[board[4]] + self.convTable[board[6]]])
    
    # Negate it if game is player2, this would mean it did all subtractions backwards
    total *= pow(-1, (self.player + 1 % 2))
    return total
  
  
  
  
  
  
  
  
  