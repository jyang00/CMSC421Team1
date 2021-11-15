# -*- coding: utf-8 -*-
"""
Pray this can be efficient
"""

# Alpha = maxes, Beta = mins
class MinimaxBot:
  
  def __init__(self, piece, oppPiece, player, heurAlg):
    # The game argument doesn't actually get used
    self.piece = piece
    self.oppPiece = oppPiece
    self.MAX_VAL = 999
    self.MIN_VAL = -999
    # The nodeTable isn't getting used right now because I don't know how to
    # keep track of duplicates efficiently
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
    def __init__(self, Outer, game, currMove, alpha, beta, isMax, player, depth):
      self.children = []
      # currMove is an integer from 1 to 26, representing which digit we're on 
      # (left to right, so 1 is the far left digit)
      self.currMove = currMove
      # Outer is a link to the MinimaxBot object so it can use certain fields
      self.Outer = Outer
      self.game = game
      self.alpha = alpha
      self.beta = beta
      self.isMax = isMax
      self.player = player
      # When incoming depth is 1, we stop
      self.depth = depth
      # Leaf is an indicator to the algorithm that this is the end of the tree
      # with leaf, we know when to start calculating heuristics
      self.leaf = False
      
      moveList = game.open_unique_moves()
      if(len(moveList) != 0 and depth > 1):
        # Try every move
        for move in moveList:
          # Make a new child with the new move and ID, with opposite isMax 
          # and player, and decremented depth
          tempGame = self.game.copy()
          if self.player == 1:
            tempGame.make_move("X", move[0], move[1])
          else:
            tempGame.make_move("O", move[0], move[1])
          child = MinimaxBot.Node(self.Outer, tempGame, move, self.alpha, self.beta, (1 + self.isMax) % 2, (self.player) % 2 + 1, depth - 1)
          self.children.append(child)
          # If duplicate, add a link from this node to that child
      # This means no children or depth = 1, so must be a leaf node
      else:
        if self.Outer.heurAlg == 1:
          self.value = self.Outer.newheuristicAlg(self.game)
        else:
          self.value = self.Outer.oldheuristicAlg(self.game)
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
              
            # Handle pruning
            if(maxVal > self.beta):
              return (maxVal, bestMove)
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
              
            # Handle pruning
            if(minVal < self.alpha):
              return (minVal, bestMove)
          return (minVal, bestMove)
      
      
    ### THIS METHOD DOES NOT GET USED IF WE DON'T HAVE NODETABLE WORKING
    # Updates the nodes with the new depth and adds new layer/s onto them
    def updateNodes(self, depth):
      self.depth = depth
      
      # If node is a leaf, add children (if possible)
      if self.leaf:
        self.leaf = False
        moveList = self.game.open_unique_moves()
        if(len(moveList) != 0 and depth > 1):
          # Try every move
          for move in moveList:
            # Make a new child with the new move and ID, with opposite isMax 
            # and player, and decremented depth
            tempGame = self.game.copy()
            if (self.player % 2) + 1 == 1:
              tempGame.make_move("X", move[0], move[1])
            else:
              tempGame.make_move("O", move[0], move[1])
            child = MinimaxBot.Node(self.Outer, tempGame, move, self.alpha, self.beta, (1 + self.isMax) % 2, (self.player)%2 + 1, depth - 1)
            self.children.append(child)
            # If duplicate, add a link from this node to that child
        # This means no children or depth = 1, so must be a leaf node
        else:
          if self.Outer.heurAlg == 1:
            self.value = self.Outer.newheuristicAlg(self.game)
          else:
            self.value = self.Outer.oldheuristicAlg(self.game)
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
    
    
  # Make the tree structure
  def calculateTree(self, currGame, depth):
    # currMove being -1 means it is the first node and there isn't a move yet
    self.root = MinimaxBot.Node(self, currGame.copy(), -1, self.MIN_VAL, self.MAX_VAL, 1, self.player, depth)
    
    return self.root.getValue()[1]
    
    
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
  
  
  
  
  
  
  
  
  