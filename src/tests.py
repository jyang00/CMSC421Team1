import unittest
import cubicTTT as ct
import randomBot as rb
import random


class TestTTT(unittest.TestCase):

    def test_random(self):
        random.seed(10571141)
        game = ct.CubicTicTacToe()
        randomBot = rb.Random_Bot(game, 'X')

        # No moves happened - This list was checked mannually for completeness and uniqueness
        # Note: It appears the top left of each face starts at 0
        avaliableUniqueMoves = [
            ('top', 0), 
            ('top', 1), 
            ('top', 2), 
            ('top', 3), 
            ('top', 4), 
            ('top', 5), 
            ('top', 6), 
            ('top', 7), 
            ('top', 8), 
            ('front', 3), 
            ('front', 4), 
            ('front', 5), 
            ('bottom', 0), 
            ('bottom', 1), 
            ('bottom', 2), 
            ('bottom', 3), 
            ('bottom', 4), 
            ('bottom', 5), 
            ('bottom', 6), 
            ('bottom', 7), 
            ('bottom', 8), 
            ('back', 3), 
            ('back', 4), 
            ('back', 5), 
            ('left', 4), 
            ('right', 4)]
        self.assertEqual(game.open_unique_moves(), avaliableUniqueMoves)

        randomBot.play_random_move(game) # This should play ('top', 8)
        avaliableUniqueMoves.remove(('top', 8))
        self.assertEqual(game.open_unique_moves(), avaliableUniqueMoves)

        randomBot.play_random_move(game) # This should play ('top', 3)
        avaliableUniqueMoves.remove(('top', 3))
        self.assertEqual(game.open_unique_moves(), avaliableUniqueMoves)

        randomBot.play_random_move(game) # This should play ('front', 4)
        avaliableUniqueMoves.remove(('front', 4))
        self.assertEqual(game.open_unique_moves(), avaliableUniqueMoves)

    
    def test_make_move(self):
        random.seed(10571141)
        game = ct.CubicTicTacToe()
        randomBot = rb.Random_Bot(game, 'X')

        board = [['-']*9 for i in range(6)]
        cube =  {
            "top":    board[0],   # Each side is a 1D list with 9 positions
            "front":  board[1], 
            "bottom": board[2],
            "back":   board[3],
            "left":   board[4],
            "right":  board[5]
        }

        randomBot.play_random_move(game) # This should play ('top', 8)
        # We would expect ('top', 8), ('right', 0), ('front', 2) to be filled with X
        cube["top"][8] = "X"
        cube["right"][0] = "X"
        cube["front"][2] = "X"
        self.assertEqual(game.cube, cube)

        randomBot.play_random_move(game) # This should play ('top', 3)
        # We would expect ('top', 3), ('left', 1) to be filled with X
        cube["top"][3] = "X"
        cube["left"][1] = "X"
        self.assertEqual(game.cube, cube)

        randomBot.play_random_move(game) # This should play ('front', 4)
        # We would expect ('front', 4)
        cube["front"][4] = "X"
        self.assertEqual(game.cube, cube)

    
    def test_check_side_win(self):
        game = ct.CubicTicTacToe()
        game.cube["front"] = ["X", "X", "X", "-", "-", "-", "-", "-", "-"]

        game.check_side_win("X", "front")
        self.assertEqual(game.x_wins, ["front"])
        self.assertEqual(game.x_score, 1)
        
        game.check_side_win("O", "front")
        self.assertEqual(game.o_wins, [])
        self.assertEqual(game.o_score, 0)

        # The logic in the method looks sound for the other 7 cases 

    def test_check_side_tie(self):
        game = ct.CubicTicTacToe()
        game.cube["front"] = ["X", "O", "X", "X", "X", "O", "O", "X", "O"]

        game.check_side_win("X", "front")
        self.assertEqual(game.x_wins, [])
        self.assertEqual(game.x_score, 0)

        game.check_side_win("O", "front")
        self.assertEqual(game.o_wins, [])
        self.assertEqual(game.o_score, 0)

        # Front is no longer winnable as it is a tie
        winnable_sides = [
            "top",
            "bottom",
            "back",
            "left",
            "right"
        ]
        game.check_side_tie("front")
        self.assertEqual(game.winnable_sides, winnable_sides)

    # The logic seems sound, but I need to play some games... 
    def check_win(self):
        game = ct.CubicTicTacToe()
        pass



if __name__ == '__main__':
    unittest.main()