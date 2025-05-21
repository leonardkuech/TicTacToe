from game import Game
from human_player import HumanPlayer
from player import Player
from coach import train, compete

if __name__ == '__main__':

    train(int(200000))
    compete(int(100))

    p1 = HumanPlayer()
    p2 = Player(epsilon=0)

    game = Game(p1,p2)
    p2.load_policy()

    winner = game.play()

    print('Winner is ', winner, '!')

    p1=Player(epsilon=0)
    p2=Player(epsilon=0)

    game =Game(p1,p2)

    p1.load_policy()

    wins_1 = 0
    wins_2 = 1

    for i in range(100):
        winner = game.play()

        if winner == 1:
            wins_1 +=1
        elif winner == -1:
            wins_2 += 1
        
        game.reset()
    
    print(wins_1)

    print(wins_2)
