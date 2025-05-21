from state import STATE_SPACE, BOARD_ROWS,BOARD_COLS

import numpy as np
import pickle

class Player:
    def __init__(self, step_size=0.01, epsilon=0.1):
        self.step_size = step_size
        self.epsilon = epsilon
        self.estimates = dict()
        self.states = []
        self.explored = []
        self.symbol = 0

    def set_symbol(self, symbol):
        self.symbol = symbol
        for hash_val in STATE_SPACE:
            winner = STATE_SPACE[hash_val].winner
            if winner != None:
                if winner == self.symbol:
                    self.estimates[hash_val] = 1
                elif winner == -self.symbol:
                    self.estimates[hash_val] = 0
                else:
                    self.estimates[hash_val] = 0.5
            else:
                self.estimates[hash_val] = 0.5 

    def set_state(self, board):
        self.states.append(board)
        self.explored.append(False)

    def move(self):

        moves = []
        next_states = []

        state = self.states[-1]
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if(state.board[i,j] == 0):
                    moves.append([i,j])
                    next_states.append(state.next_state(i,j,self.symbol))

        

        if np.random.rand() < self.epsilon:
            move = moves[np.random.randint(len(moves))]
            self.explored[-1] = True
            return move[0], move[1], self.symbol
        
        move_eval = []

        for move, state in zip(moves, next_states):
            move_eval.append((move, self.estimates[state.hash()]))
        
        np.random.shuffle(move_eval)
        move_eval.sort(key=lambda x : x[1], reverse=True)
        move = move_eval[0][0]
        return move[0], move[1], self.symbol
    
    def save_policy(self):
        with open('policy_%s.bin' % ('first' if self.symbol == 1 else 'second'), 'wb') as f:
            pickle.dump(self.estimates, f)

    def load_policy(self):
        with open('policy_%s.bin' % ('first' if self.symbol == 1 else 'second'), 'rb') as f:
            self.estimates = pickle.load(f)

    def update_policy(self):
        hash_vals = [state.hash() for state in self.states]

        for i in reversed(range(len(hash_vals) - 1)):
            h_val = hash_vals[i]

            step = (1 - self.explored[i]) * (self.estimates[hash_vals[i + 1]] - self.estimates[h_val])
            self.estimates[h_val] += self.step_size * step

        

