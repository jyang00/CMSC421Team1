import minimaxbot
import tictactoe

NUM_ITERATIONS = 10

tictactoe = tictactoe.tictactoe()
minimaxbot = minimaxbot.minimaxbot()

firstPlayerWins = 0
secondPlayerWins = 0

counter = 0
while counter < NUM_ITERATIONS:

    firstPlayerFacesWon = 0
    secondPlayerFacesWon = 0

    # While there are avaliable moves in the game: 
    firstPlayerMove = minimaxbot.getNextMove(tictactoe.gameBoard)
    secondPlayerMove = minimaxbot.getNextMove(tictactoe.gameBoard)
    tictactoe.updateGame()
    # Update faces won

    
    if firstPlayerFacesWon > secondPlayerFacesWon:
        firstPlayerWins += 1
    elif firstPlayerFacesWon < secondPlayerFacesWon: 
        secondPlayerWins += 1

    counter += 1

print("First player won {} times while second player won {} times.".format(firstPlayerWins, secondPlayerWins))

