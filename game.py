from state import State, STATE_SPACE


SYMBOL_P1 = 1
SYMBOL_P2 = -1

class Game:
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.p1.set_symbol(SYMBOL_P1)
        self.p2.set_symbol(SYMBOL_P2)
        self.state = None

    def turn(self):
        while True:
            yield self.p1
            yield self.p2

    def broadcast_state(self):

        self.p1.set_state(self.state)
        self.p2.set_state(self.state)

    def play(self, print_state=False):
        turn = self.turn()
        self.state = State()
        self.broadcast_state()

        if print_state:
            self.state.print_board()

        while self.state.winner == None:
            current_player = next(turn)
            i,j,symbol = current_player.move()
            if self.state.board[i][j] == 0:

                new_state = self.state.next_state(i,j,symbol)
                new_hash = new_state.hash()
                

                new_state = STATE_SPACE[new_hash]

                self.state = new_state
                self.broadcast_state()

                if print_state:
                    self.state.print_board()
        
        return self.state.winner
    
    def reset(self):
        self.p1.states = []
        self.p1.explored = []

        self.p2.states = []
        self.p2.explored = []

        self.state = None