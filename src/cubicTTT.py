import numpy as np
import random
import copy
import time as tI
# Let me know if any changes are needed

class CubicTicTacToe:
    def __init__(self):
        self.board = [['-']*9 for i in range(6)] # Game board is a 2D list containing all sides.
        self.cube =  {"top":    self.board[0],   # Each side is a 1D list with 9 positions
                      "front":  self.board[1], 
                      "bottom": self.board[2],
                      "back":   self.board[3],
                      "left":   self.board[4],
                      "right":  self.board[5]}
        self.open_moves = [[i for i in range(9)] for i in range(6)]          # Elements get removed on moves made (avoids extra computing)
        self.sides =          ["top","front","bottom","back","left","right"] # I use to match indices to string for sides
        self.winnable_sides = ["top","front","bottom","back","left","right"] # Elements get removed as they are won
        self.unique_moves = self.generate_unique_moves()
        self.sides_tied =  []
        self.player_list = ["X", "O"] # Used in random first player
        self.x_score = 0 
        self.x_moves = []  # excludes sides touched
        self.x_wins =  []  # sides won
        self.o_score = 0
        self.o_wins =  []
        self.o_moves = []
        self.is_game_over = False
        self.game_winner = None # None if tied game
        self.time1 = 0
        self.time2 = 0
        
        
        
        
    
    # X is always first player by convention?
    def first_player(self):
        return "X"

    def second_player(self):
        return "O"

    # (Alternative) randomly pick first player.
    # Call again to get the second player.
    def random_player(self):
        if len(self.player_list) == 1: 
            return self.player_list[0]
        rand = random.randint(0,len(self.player_list)-1)
        return self.player_list.pop(rand)

    # For the various open move methods below
    #   I tried to provide two versions:
    #       (1) that returns just 1D/2D lists
    #       (2) that returns 1D list of tuples (might be easier to follow/debug)
    #
    # - Not the best naming schemes, sorry lol
    # - We should remove copying if no one is 100% not modifying the return lists for performance?

    # 2D list representation for the total possible board moves
    def open_board_moves_list(self):
        return copy.deepcopy(self.open_moves) 

    # 1D List representation for the possible moves for the given side.
    def open_side_moves_list(self, side):
        return copy.copy(self.open_moves[self.sides.index(side)])

    # 2D list representation of the total possible moves (EXCLUDES won sides)
    def open_unwon_moves_list(self):
        res = []
        for s in range(6):
            res.append([])
            if self.sides[s] in self.winnable_sides:
                res[s] = copy.copy(self.open_moves[s])
        return res             

    # Tuple(side,pos) representation of the total possible moves
    def open_board_moves(self):
        res = []
        for s in range(6):
            for p in self.open_moves[s]:
                res.append((self.sides[s],p))
        return res

    # Tuple(side,pos) representation of the possible moves for given side.
    def open_side_moves(self, side):
        side = self.side_string(side)
        res = []
        for pos in range(9):
            if self.cube[side][pos] == '-':
                res.append((side,pos))
        return res

    # Tuple(side,pos) representation of the total possible moves (Excludes won sides)
    def open_unwon_moves(self):
        res = []
        for s in range(6):
            if self.sides[s] in self.winnable_sides:
                for p in self.open_moves[s]:
                    res.append((self.sides[s],p))
        return res

    # Tuple representation of the 26 unique moves
    def open_unique_moves(self):
        open = self.open_board_moves()
        res = []
        for i in open:
            if i in self.unique_moves:
                res.append(i)
        return res

    # Performs a move for the player
    def make_move(self, player, side, pos):
        side = self.side_string(side)

        if not self.can_move(side,pos): #or self.is_game_over:
            return False # Invalid move / Game ended
        
        if player == "X": 
            self.x_moves.append((side,pos))
        if player == "O": 
            self.o_moves.append((side,pos))  
        if pos in self.open_moves[self.sides.index(side)]: 
            self.open_moves[self.sides.index(side)].remove(pos)
        
        self.move_piece(player,side,pos)  # Perform Move
       
        # Added: just to check the current side
        self.check_side_win(player,side)    # Check side wins/ties 
        self.check_side_tie(side)
        #
        
        self.touch_edges(player,side,pos) # Move on edges
        self.check_win()       
        
        return True

    # Checks if position is open
    def can_move(self, side, pos):
        side = self.side_string(side)
        return self.cube[side][pos] == '-'

    # (You should be calling make_move instead)
    def move_piece(self, player, side, pos):
        self.cube[side][pos] = player
        
    # Handles moves crossing over to touched edges  
    def touch_edges(self, player, side, pos):
        touching_edges = { # lol don't judge
            "top":      [[("back",2),("left",0)],[("back",1)],[("back",0),("right",2)],[("left",1)],   [],  [("right",1)], [("front",0),("left",2)],[("front",1)],[("front",2),("right",0)]],
            "front":    [[("left",2),("top",6)],[("top",7)],[("top",8),("right",0)],[("left",5)],      [],  [("right",3)],[("left",8),("bottom",0)],[("bottom",1)],[("bottom",2),("right",6)]],
            "bottom":   [[("left",8),("front",6)],[("front",7)],[("front",8),("right",6)],[("left",7)],[],  [("right",7)],[("left",6),("back",8)],[("back",7)],[("back",6),("right",8)]],
            "back":     [[("top",2),("right",2)],[("top",1)],[("top",0),("left",0)],[("right",5)],     [],  [("left",3)],[("right",8),("bottom",8)],[("bottom",7)],[("bottom",6),("left",6)]],
            "left":     [[("top",0),("back",2)],[("top",3)],[("top",6),("front",0)],[("back",5)],      [],  [("front",3)],[("back",8),("bottom",6)],[("bottom",3)],[("front",6),("bottom",0)]],
            "right":    [[("front",2),("top",8)],[("top",5)],[("top",2),("back",0)],[("front",5)],     [],  [("back",3)],[("front",8),("bottom",2)],[("bottom",5)],[("bottom",8),("back",6)]]}
        for i in touching_edges[side][pos]:
            self.move_piece(player,i[0],i[1]) 
            # Added: check for each side that has changed
            self.check_side_win(player,i[0])   # Check side wins/ties 
            self.check_side_tie(i[0])
            #
            if i[1] in self.open_moves[self.sides.index(i[0])]:
                self.open_moves[self.sides.index(i[0])].remove(i[1])
      
    def check_win(self):
        if len(self.sides_tied) == 6:
            self.is_game_over = True
            self.game_winner = None
            return

        # if not self.winnable_sides:
        #     self.is_game_over = True
        #     if self.x_score > self.o_score:
        #         self.game_winner = "X"
        #     else:
        #         self.game_winner = "O"
                
        if self.x_score >= 4:
            self.is_game_over = True
            self.game_winner = "X"
            return
        
        if self.o_score >= 4:
            self.is_game_over = True
            self.game_winner = "O"
            return
            
    def check_side_win(self, player, side):
        side = self.side_string(side)
        s = self.cube[side]
        won = False
        winnable_pos = [(0,1,2),(3,4,5),(6,7,8), # rows
                        (0,3,6),(1,4,7),(2,5,8), # cols
                        (0,4,8),(2,4,6)]         # diagonals

        if side not in self.winnable_sides:
            return

        for (a,b,c) in winnable_pos:
            if s[a] + s[b] + s[c] == player*3:
                won = True
        if won:
            self.winnable_sides.remove(side)
            if player == "X":
                self.x_score += 1
                self.x_wins.append(side)
            if player == "O":
                self.o_score += 1
                self.o_wins.append(side)

    # A tie is a side that is full with no winner
    def check_side_tie(self, side):
        side = self.side_string(side)
        
        if side not in self.winnable_sides:
            return
        # Changed: instead of having a count for '-', 
        #           just return when '-' is seen
        for i in range(9): # check for tie
            if self.cube[side][i] == '-':
               return
             
        # update winnable states
        self.sides_tied.append(side)
        self.winnable_sides.remove(side) 
        #

    # A helper method. Pass in int to get corresponding string side
    # Index 0 = Top Board, Index 1 = Front board, etc.
    def side_string(self, side):
        if side not in self.sides: side = self.sides[side]
        return side

    # called on gameboard initialization.
    def generate_unique_moves(self):
        res = set() # 26 unique moves
        for s in self.cube: # centers
            res.add((s,4))
        for p in range(9):  # entire top and bottom
            res.add(("top",p))
            res.add(("bottom",p))
        for s in ["front","back"]: # positions 3 and 5 for front and back
            res.add((s,3))
            res.add((s,5))
        return res

    # Prints out current state of each 1D board
    def display_boards(self):
        for k in self.cube: print(f"{k}:\t {self.cube[k]}")

    def display_stats(self):
        print('-'*40)
        print(f"X Score:{self.x_score}")
        print(f"X wins:{self.x_wins}")
        print(f"X moves:{self.x_moves}\n")
        print(f"O Score:{self.o_score}")
        print(f"O wins:{self.o_wins}")
        print(f"O moves:{self.o_moves}\n")
        print(f"Tied Sides:{self.sides_tied}")
        print(f"winnable Sides:{self.winnable_sides}")
        print(f"Game over:{self.is_game_over}")
        print(f"Game winner:{self.game_winner}")
        print('-'*40)

    # Prints the current state of the game board like an unraveled cube.
    def display_game(self):
        top     = np.array(self.cube["top"]).reshape(3,3)
        front   = np.array(self.cube["front"]).reshape(3,3) 
        left    = np.array(self.cube["left"]).reshape(3,3)
        right   = np.array(self.cube["right"]).reshape(3,3)
        bottom  = np.array(self.cube["bottom"]).reshape(3,3)
        back    = np.flipud(np.fliplr(np.array(self.cube["back"]).reshape(3,3))) # back Gets flipped in this perspective

        print('\n%30s' % ("TOP"))
        for i in top:
            print('%30s' % (i))

        print('%15s%15s%15s' % ("LEFT", "FRONT", "RIGHT") )
        for a,b,c in zip(left,front,right):
            print('%15s%15s%15s' % (a,b,c))

        print('%30s' % ("BOTTOM")) 
        for i in bottom:
            print('%30s' % (i))

        print('%30s' % ("BACK"))  
        for i in back:
            print('%30s' % (i))

    # Not entirely sure how impactful deepcopy 
    # will have on performance with the amount we copy
    def copy(self):
      return copy.deepcopy(self)
  
      
      
      
      
      
      
      
      
      
      
      
      