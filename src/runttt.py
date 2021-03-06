import minimaxbot
import cubicTTT as ct
import randomBot as rb
import random

NUM_ITERATIONS = 25

def run_ttt():

    randomBotWins = 0
    mmbWins = 0

    counter = 0
    while counter < NUM_ITERATIONS:

        game = ct.CubicTicTacToe()

        order = random.randint(0, 1)

        if order == 1:
            # print("RB goes first")
            randomBot = rb.Random_Bot(game, 'X')
            mmb = minimaxbot.MinimaxBot('O', 'X', 2, 1)
        else:
            # print("MMB first")
            mmb = minimaxbot.MinimaxBot('X', 'O', 1, 1)
            randomBot = rb.Random_Bot(game, 'O')
        

        moveNum = 1
        while game.is_game_over == False:
            
            print("------------------------------------------------------")
            print("-----------------------Turn " + str(moveNum) + "-------------------------")
            print("------------------------------------------------------")
    
            if (order == 1):
                randomBot.play_random_move(game)

                if (game.is_game_over):
                    game.display_boards()
                    break

                mmbMove = mmb.calculateTree(game, 4)
                game.make_move(mmb.piece, mmbMove[0], mmbMove[1])

            else:
                mmbMove = mmb.calculateTree(game, 4)
                game.make_move(mmb.piece, mmbMove[0], mmbMove[1])

                if (game.is_game_over):
                    game.display_boards()
                    break

                randomBot.play_random_move(game)

            game.display_boards() 

            moveNum += 1

        winner = game.game_winner
        if winner == 'X' and order == 1:
            randomBotWins += 1
            print("Random Bot won with X")
        elif winner == 'O' and order == 1:
            mmbWins += 1
            print("MMB won with X")
        elif winner == 'X' and order == 0:
            mmbWins += 1
            print("MMB won with O")
        elif winner == 'O' and order == 0:
            randomBotWins += 1
            print("Random Bot won with O")

        print(game.x_moves)
        print(game.o_moves)
        counter += 1

    print("RandomBot won {} times while MinimaxBot won {} times.".format(randomBotWins, mmbWins))

if __name__ == '__main__':
    run_ttt()