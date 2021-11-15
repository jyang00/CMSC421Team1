import minimaxbot
import cubicTTT as ct
import randomBot as rb
import random

NUM_ITERATIONS = 5
DEBUG = True


def run_ttt():

    randomBotWins = 0
    mmbWins = 0

    counter = 0
    while counter < NUM_ITERATIONS:

        game = ct.CubicTicTacToe()

        order = random.randint(0, 1)

        if order == 1:
            print("RB goes first")
            randomBot = rb.Random_Bot(game, 'X')
            mmb = minimaxbot.MinimaxBot(game, 'O', 'X', 2)
        else:
            print("MMB first")
            mmb = minimaxbot.MinimaxBot(game, 'X', 'O', 1)
            randomBot = rb.Random_Bot(game, 'O')
        
        moveNum = 1
        while game.is_game_over == False:


            if (order == 1):

                if DEBUG:
                    print("------------------------------------------------------")
                    print("-----------------------Turn " + str(moveNum) + "-------------------------")
                    print("------------------------------------------------------")
                    randomBot.play_random_move(game)
                    game.display_boards()

                    print("------------------------------------------------------")
                    mmb.calculateTree(game, 5)
                    mmbMove = mmb.evalPosition(game)
                    game.make_move(mmb.piece, mmbMove[0], mmbMove[1])
                    game.display_boards()
                else:
                    randomBot.play_random_move(game)
                    mmb.calculateTree(game, 5)
                    mmbMove = mmb.evalPosition(game)
                    game.make_move(mmb.piece, mmbMove[0], mmbMove[1])

            else:

                if DEBUG: 
                    print("------------------------------------------------------")
                    print("-----------------------Turn " + str(moveNum) + "-------------------------")
                    print("------------------------------------------------------")
                    mmb.calculateTree(game, 5)
                    mmbMove = mmb.evalPosition(game)
                    game.make_move(mmb.piece, mmbMove[0], mmbMove[1])
                    game.display_boards()

                    print("------------------------------------------------------")
                    randomBot.play_random_move(game)
                    game.display_boards()
                else:
                    mmb.calculateTree(game, 5)
                    mmbMove = mmb.evalPosition(game)
                    game.make_move(mmb.piece, mmbMove[0], mmbMove[1])
                    randomBot.play_random_move(game)

            moveNum += 1

        winner = game.game_winner
        if winner == 'X' and order == 1:
            randomBotWins += 1
        elif winner == 'O' and order == 1:
            mmbWins += 1
        elif winner == 'X' and order == 0:
            mmbWins += 1
        elif winner == 'O' and order == 0:
            randomBotWins += 1

        counter += 1

    print("RandomBot won {} times while MinimaxBot won {} times.".format(randomBotWins, mmbWins))

if __name__ == '__main__':
    run_ttt()

