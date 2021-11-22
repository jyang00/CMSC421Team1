import unittest
import cubicTTT as ct
import randomBot as rb
import random


class TestTTT(unittest.TestCase):

    def test_random(self):
        self.maxDiff = None
        random.seed(10571141)
        game = ct.CubicTicTacToe()
        randomBot = rb.Random_Bot(game, 'X')

        # No moves happened
        # Note: It appears the top left of each face starts at 0
        avaliableMoves = [
            ('top', 0), ('top', 1), ('top', 2), 
            ('top', 3), ('top', 4), ('top', 5), 
            ('top', 6), ('top', 7), ('top', 8), 
            ('front', 0), ('front', 1), ('front', 2), 
            ('front', 3), ('front', 4), ('front', 5), 
            ('front', 6), ('front', 7), ('front', 8), 
            ('bottom', 0), ('bottom', 1), ('bottom', 2), 
            ('bottom', 3), ('bottom', 4), ('bottom', 5), 
            ('bottom', 6), ('bottom', 7), ('bottom', 8), 
            ('back', 0), ('back', 1), ('back', 2), 
            ('back', 3), ('back', 4), ('back', 5), 
            ('back', 6), ('back', 7), ('back', 8), 
            ('left', 0), ('left', 1), ('left', 2), 
            ('left', 3), ('left', 4), ('left', 5), 
            ('left', 6), ('left', 7), ('left', 8), 
            ('right', 0), ('right', 1), ('right', 2), 
            ('right', 3), ('right', 4), ('right', 5), 
            ('right', 6), ('right', 7), ('right', 8)
        ]
        self.assertEqual(game.open_board_moves(), avaliableMoves)

        # Random generates 16 which corresponds to ('front', 7)
        randomBot.play_random_move(game)
        avaliableMoves.remove(('front', 7))
        avaliableMoves.remove(('bottom', 1))
        self.assertEqual(game.open_board_moves(), avaliableMoves)
        self.assertEqual(len(game.open_board_moves()), 52)

        # Random generates 6 which corresponds to ('top', 6)
        randomBot.play_random_move(game) 
        avaliableMoves.remove(('top', 6))
        avaliableMoves.remove(('front', 0))
        avaliableMoves.remove(('left', 2))
        self.assertEqual(game.open_board_moves(), avaliableMoves)
        self.assertEqual(len(game.open_board_moves()), 49)

        # Random generates 16 which corresponds to ('bottom', 2)
        randomBot.play_random_move(game) 
        avaliableMoves.remove(('bottom', 2))
        avaliableMoves.remove(('front', 8))
        avaliableMoves.remove(('right', 6))
        self.assertEqual(game.open_board_moves(), avaliableMoves)
        self.assertEqual(len(game.open_board_moves()), 46)

    def test_make_move(self):
        random.seed(10571141)
        game = ct.CubicTicTacToe()
        randomBot = rb.Random_Bot(game, 'X')

        board = [['-']*9 for i in range(6)]
        cube =  {
            "top":    board[0],
            "front":  board[1], 
            "bottom": board[2],
            "back":   board[3],
            "left":   board[4],
            "right":  board[5]
        }

        # Random generates 16 which corresponds to ('front', 7)
        randomBot.play_random_move(game)
        cube["front"][7] = "X"
        cube["bottom"][1] = "X"
        self.assertEqual(game.cube, cube)

        # Random generates 6 which corresponds to ('top', 6)
        randomBot.play_random_move(game) 
        cube["top"][6] = "X"
        cube["front"][0] = "X"
        cube["left"][2] = "X"
        self.assertEqual(game.cube, cube)

        # Random generates 16 which corresponds to ('bottom', 2)
        randomBot.play_random_move(game) 
        cube["bottom"][2] = "X"
        cube["front"][8] = "X"
        cube["right"][6] = "X"
        self.assertEqual(game.cube, cube)
    
    def test_check_side_win(self):
        game = ct.CubicTicTacToe()
        game.make_move("X", "front", 0)
        game.make_move("X", "front", 1)
        game.make_move("X", "front", 2)

        self.assertCountEqual(game.x_wins, ["front", "top"])
        self.assertEqual(game.x_score, 2)
        
        self.assertCountEqual(game.o_wins, [])
        self.assertEqual(game.o_score, 0)

        self.assertEqual(len(game.open_unwon_moves()), 54-18-2)

        # The logic in the method looks sound for the other 7 cases 

    def test_check_side_tie(self):
        game = ct.CubicTicTacToe()
        
        game.make_move("X", "front", 0)
        self.assertEqual(len(game.open_unwon_moves()), 51)
        game.make_move("O", "front", 1)
        self.assertEqual(len(game.open_unwon_moves()), 49)
        game.make_move("X", "front", 2)
        self.assertEqual(len(game.open_unwon_moves()), 46)
        game.make_move("X", "front", 3)
        self.assertEqual(len(game.open_unwon_moves()), 44)
        game.make_move("X", "front", 4)
        self.assertEqual(len(game.open_unwon_moves()), 43)
        game.make_move("O", "front", 5)
        self.assertEqual(len(game.open_unwon_moves()), 41)
        game.make_move("O", "front", 6)
        self.assertEqual(len(game.open_unwon_moves()), 38)
        game.make_move("X", "front", 7)
        self.assertEqual(len(game.open_unwon_moves()), 36)
        game.make_move("O", "front", 8)
        self.assertEqual(len(game.open_unwon_moves()), 33)

        self.assertCountEqual(game.x_wins, [])
        self.assertEqual(game.x_score, 0)

        self.assertCountEqual(game.o_wins, [])
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

    def check_minimax_bot(self):
        pass


if __name__ == '__main__':
    unittest.main()