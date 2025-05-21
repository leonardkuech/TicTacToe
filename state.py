import numpy as np
import sys

BOARD_ROWS = 3
BOARD_COLS = 3

class State:
    def __init__(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.hash_val = None
        self.winner = None
    
    # compute unique hash value to reference state
    def hash(self):
        if self.hash_val is None:
            self.hash_val = 0
            for i in np.nditer(self.board):
                self.hash_val = self.hash_val * 3 + i + 1
        return self.hash_val
    
    #checks if a game is over and returns the winner
    def check_game_over(self):
        if self.winner is None:

            board_sum = np.sum(np.abs(self.board))
            if board_sum == BOARD_ROWS * BOARD_COLS:
                self.winner = 0
            
            sums = []

            for i in range(BOARD_ROWS):
                sums.append(np.sum(self.board[i,:]))
            for i in range(BOARD_COLS):
                sums.append(np.sum(self.board[:,i]))

            trace, reverse_trace = 0, 0

            for i in range(BOARD_ROWS):
                trace += self.board[i,i]
                reverse_trace += self.board[i,BOARD_ROWS-i-1]

            sums.append(trace)
            sums.append(reverse_trace)

            for sum in sums:
                if sum == 3:
                    self.winner = 1
                
                if sum == -3:
                    self.winner = -1

        return self.winner

    #Clones board state into new object and applies move made 
    def next_state(self, i,j,symbol):
        new_state = State()
        new_state.board = np.copy(self.board)
        new_state.board[i,j] = symbol
        return new_state
    
    def print_board(self):
        print('------------------')
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                symbol = self.board[i,j]
                if symbol == 1:
                    print('| X | ', end = "")
                elif symbol == -1:
                    print('| O | ', end="")
                else:
                    print('|   | ', end = "")
            print()
            print('------------------')

def get_all_states_impl(current_state, current_symbol, all_states):
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if current_state.board[i][j] == 0:
                new_state = current_state.next_state(i, j, current_symbol)
                new_state.check_game_over()
                new_hash = new_state.hash()
                if new_hash not in all_states:
                    all_states[new_hash] = (new_state)
                    if new_state.winner == None:
                        get_all_states_impl(new_state, -current_symbol, all_states)


def get_all_states():
    current_symbol = 1
    current_state = State()
    all_states = dict()
    all_states[current_state.hash()] = (current_state)
    get_all_states_impl(current_state, current_symbol, all_states)
    return all_states


# all possible board configurations
STATE_SPACE = get_all_states()