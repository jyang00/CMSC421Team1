# -*- coding: utf-8 -*-
"""
Minimax bot
"""

# Alpha = maxes, Beta = mins
class MinimaxBot:
  
  def __init__(self, piece, oppPiece, player, heurAlg):
    # The game argument doesn't actually get used
    self.piece = piece
    self.oppPiece = oppPiece
    self.MAX_VAL = 999
    self.MIN_VAL = -999
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
    self.count = 0
    
  class Node:
    # This is a node for the minimax tree structure
    
    
    # Setup fields and create a bunch of child nodes
    # If a leaf, set fields to indicate that and evaluate current position
    def __init__(self, Outer, game, alpha, beta, isMax, player, depth):
      self.children = []
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
      # With self.leaf, we know when to start calculating heuristics
      self.leaf = False
      self.value = 0
      
      moveList = game.open_unique_moves()
      if(len(moveList) != 0 and depth > 1):
        # Try every move
        for move in moveList:
          # Make a new child with the new move, with opposite isMax 
          # and player, and decremented depth
          tempGame = self.game.copy()
          if self.player == 1:
            tempGame.make_move("X", move[0], move[1])
          else:
            tempGame.make_move("O", move[0], move[1])
          
          child = MinimaxBot.Node(self.Outer, tempGame, self.alpha, self.beta, (1 + self.isMax) % 2, (self.player) % 2 + 1, depth - 1)
          self.children.append((move, child))
          if self.isMax:
            self.alpha = max(self.alpha, child.beta)
            if self.alpha > self.beta:
              self.Outer.count += 1
              break
          else:
            self.beta = min(self.beta, child.alpha)
            if self.beta < self.alpha:
              self.Outer.count += 1
              break
      # This means no children or depth = 1, so must be a leaf node
      else:
        if self.Outer.heurAlg == 1:
          self.value = self.Outer.newheuristicAlg(self.game)
        else:
          self.value = self.Outer.oldheuristicAlg(self.game)
        self.leaf = True
        if self.isMax:
          self.alpha = self.value
        else:
          self.beta = self.value

    
    
    # Returns the best value along with the move used to get there
    def getValue(self):
      ### Leaves never have this method called right now
      if (self.leaf):
        #return (self.value, self.currMove)
        return (self.value, ("-", 0))
      else:
        # If max node, use alpha + maxes
        if self.isMax:
          maxVal = self.Outer.MIN_VAL
          for (move, child) in self.children:
            result = (child.beta, move)
            currVal = result[0]
            if(currVal > maxVal):
              maxVal = currVal
              bestMove = result[1]
          return (maxVal, bestMove)
        # If min node, use beta + mins
        else:
          minVal = self.Outer.MAX_VAL
          for (move, child) in self.children:
            result = (child.alpha, move)
            currVal = result[0]
            if(currVal < minVal):
              minVal = currVal
              bestMove = result[1]
          return (minVal, bestMove)
       
    
  # Make the tree structure
  def calculateTree(self, currGame, depth):
    self.nodeTable = {}
    self.root = MinimaxBot.Node(self, currGame.copy(), self.MIN_VAL, self.MAX_VAL, 1, self.player, depth)
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
  
  
  
  
  
  
  
  
  