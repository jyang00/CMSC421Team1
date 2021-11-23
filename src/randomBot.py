import random as r

class Random_Bot:

    def __init__(self, game, player):
        self.game = game
        self.player = player

    def get_rand_move(self, curr_game):
        total_moves = curr_game.open_board_moves()
        rand_int = r.randrange(0, len(total_moves), 1)
        return total_moves[rand_int]

    def play_random_move(self, curr_game):
        move = self.get_rand_move(curr_game)
        curr_game.make_move(self.player, move[0], move[1])