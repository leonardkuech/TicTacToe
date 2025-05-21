from player import Player
from game import Game

def train(epochs, print_epochs=1000):
    player1 = Player(epsilon=0.01)
    player2 = Player(epsilon=0.01)

    player1_wins = 0.0
    player2_wins = 0.0

    game = Game(player1,player2)

    for i in range(1,epochs+1):
        winner = game.play()

        if winner == 1:
            player1_wins+=1
        elif winner == -1:
            player2_wins+=1

        player1.update_policy()
        player2.update_policy()


        if i % print_epochs == 0:
            print(f'Player 1 winrate: {player1_wins/i:.03f} % | Player 2 wins: {player2_wins/i:.03f} % | Total Games: {i}' )

        game.reset()

    player1.save_policy()
    player2.save_policy()

def compete(rounds):
    player1 = Player(epsilon=0)
    player2 = Player(epsilon=0)

    game = Game(player1,player2)

    player1.load_policy()
    player2.load_policy()

    player1_wins = 0.0
    player2_wins = 0.0

    for i in range(rounds):
        winner = game.play()
        if winner == 1:
            player1_wins+=1
        elif winner == -1:
            player2_wins+=1
        game.reset()


    print(f'Player 1 winrate: {player1_wins/rounds} % | Player 2 wins: {player2_wins/rounds} % | Total Games: {rounds}' )



        




