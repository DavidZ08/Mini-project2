# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import sys
import numpy as np


# Method that will be used to prompr the user for an integer and check that it is within bounds.
def int_extraction(question, bound1, bound2):
    while True:
        try:
            print(question)
            user_input = int(input())
        except ValueError:
            print("Wrong input. Please try again.")
            continue
        if user_input < bound1 or user_input > bound2:
            print("Value out of bounds. Please try again")
            continue
        else:
            return user_input


# Method that will prompt the user for a boolean.
def boolean_extraction(question, bound1, bound2):
    user_input = int_extraction(question, bound1, bound2)
    if (user_input == 1):
        return False
    else:
        return True


# Method that will prompt the user for the positions of the blocs.
def blocposition_extraction(board_size, bloc_number):
    coordinates_list = list()
    x_pos = 0
    y_pos = 0
    for i in range(bloc_number):
        while not int(x_pos) in range(0, board_size):
            print("Enter the x coordinate of your bloc.")
            x_pos_string = input()
            x_pos = coordinate_extraction(x_pos_string)
        while not int(y_pos) in range(0, board_size):
            print("Enter the y coordinate of your bloc.")
            y_pos = input()
        coordinate_tuple = (x_pos, y_pos)
        coordinates_list.append(coordinate_tuple)
    return coordinates_list


# Method that will be used to prompt the user for the various parameters needed to initiate a game.
def input_extraction():
    n = int_extraction("Please enter the size of the board [3, 10]", 3, 10)
    b = int_extraction(
        "Please enter the number of blocs [2, 2*sizeofboard]", 3, 2*n)
    s = int_extraction(
        "Please enter the winning line-up size [3, sizeofboard]", 3, n)
    coordinates_list = blocposition_extraction(n-1, b)
    d1 = int_extraction(
        "Please enter the maximum depth of the adverserial search d1 [1, sizeofboard]", 1, n-1)
    d2 = int_extraction(
        "Please enter the maximum depth of the adverserial search d2 [1, sizeofboard]", 1, n-1)
    t = int_extraction(
        "Please enter the maximum allowed time for the program to return a move", 1, float('inf'))
    a = int_extraction(
        "To force the use of minimax, enter '0'. To force the use of alphabeta, enter '1'", 0, 1)
    play_mode = int_extraction(
        "Please enter the game mode: 1. H-H, 2. H-AI, 3. AI-H, 4. AI-AI", 1, 4)
    return n, b, s, coordinates_list, d1, d2, t, a, play_mode


# Method that will be used to convert aphabetical coordinates to numerical ones.
def coordinate_extraction(str):
    alphabet_coordinates = {'A': 0, 'B': 1, 'C': 2, 'D': 3,
                            'E': 4, 'F': 5, 'H': 6, 'I': 7, 'J': 8, 'K': 9}
    return alphabet_coordinates[str]


# Method that will be used to prompt the user for coordinates.
def move_extraction_human(board_size):
    # TODO: finish this method for human players, gives them only one chance to re-enter their move. In case of another failure, makes player lose the game.
    print("Enter the x coordinate of your move.")
    x_pos_string = input()
    x_pos = coordinate_extraction(x_pos_string)
    if (x_pos > board_size or x_pos < 0):
        print("Enter the y coordinate of your move.")
    y_pos = input()
    coordinate_tuple = (x_pos, y_pos)
    return coordinate_tuple

# TODO: Finish method for AI players, gives them 0 chances.


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3
    n = 0
    b = 0
    s = 0
    coordinates_list = list()
    d1 = 0
    d2 = 0
    t = 0
    a = True
    play_mode = 0

    def __init__(self, n, b, s, coordinates_list, d1, d2, t, a, play_mode, recommend=True):
        self.n, self.b, self.s, self.coordinates_list, self.d1, self.d2, self.t, self.a, self.play_mode = n, b, s, coordinates_list, d1, d2, t, a, play_mode
        self.initialize_game()
        self.recommend = recommend

    def initialize_game(self):
        self.current_state = [
            ['.'for i in range(self.n)] for j in range(self.n)]
        for i in self.coordinates_list:
            self.current_state[i[0]][i[1]] = 'b'
        # Player ◦ always plays first
        self.player_turn = '◦'

    def draw_board(self):
        print()
        for y in range(0, self.n):
            for x in range(0, self.n):
                print(F'{self.current_state[y][x]}', end="")
            print()
        print()

    def is_valid(self, px, py):
        if px < 0 or px > self.n-1 or py < 0 or py > self.n-1:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):

        # Vertical win
        vertical_counter = 0
        for i in range(0, self.n):
            for j in range(1, self.n):
                if (self.current_state[j-1][i] != '.' and self.current_state[j-1][i] != 'b' and self.current_state[j-1][i] == self.current_state[j][i]):
                    vertical_counter += 1
                    if vertical_counter == self.s-1:
                        return self.current_state[j][i]
                    else:
                        continue
                else:
                    vertical_counter = 0
                    continue
            # It has to check every column completely for a vertical win before moving on to check for a horizontal win
            vertical_counter = 0

        # Horizontal win
        horizontal_counter = 0
        for i in range(0, self.n):
            for j in range(1, self.n):
                if (self.current_state[i][j-1] != '.' and self.current_state[i][j-1] != 'b' and self.current_state[i][j-1] == self.current_state[i][j]):
                    horizontal_counter += 1
                    if horizontal_counter == self.s-1:
                        return self.current_state[i][j]
                    else:
                        continue
                else:
                    horizontal_counter = 0
                    continue
            horizontal_counter = 0

        diagonal_counter = 0
        # First set of diagonals from top left to bottom right
        for i in range(1, self.n):  # check for a win on the main diagonal
            if (self.current_state[i-1][i-1] != '.' and self.current_state[i-1][i-1] != 'b' and self.current_state[i-1][i-1] == self.current_state[i][i]):
                diagonal_counter += 1
                if diagonal_counter == self.s-1:
                    return self.current_state[i][i]
            else:
                diagonal_counter = 0
        if (self.n > self.s):  # check for a win on the remaining diagonals
            diagonal1_counter = 0
            diagonal2_counter = 0
            for i in range(1, self.n-self.s):
                for j in range(1, self.n-i):
                    if (self.current_state[j-1][i+j-1] != '.' and self.current_state[j-1][i+j-1] != 'b' and self.current_state[j-1][i+j-1] == self.current_state[j][i+j]):
                        diagonal1_counter += 1

                        if diagonal_counter == self.s-1:
                            return self.current_state[j][i+j]
                    else:
                        diagonal2_counter = 0

                    if (self.current_state[i+j-1][j-1] != '.' and self.current_state[i+j-1][j-1] != 'b' and self.current_state[i+j-1][j-1] == self.current_state[i+j][j]):
                        diagonal2_counter += 1

                        if diagonal_counter == self.s-1:
                            return self.current_state[i][i+j]
                    else:
                        diagonal2_counter = 0
                diagonal1_counter = 0
                diagonal2_counter = 0

        # Second set of diagonals from top right to bottom left
        # Flip the matrix
        diagonal_counter = 0
        current_state_flipped = []
        for i in range(len(self.current_state)):
            current_state_flipped.append(self.current_state[i][::-1])

        for i in range(1, self.n):  # check for a win on the main diagonal
            if (current_state_flipped[i-1][i-1] != '.' and current_state_flipped[i-1][i-1] != 'b' and current_state_flipped[i-1][i-1] == current_state_flipped[i][i]):
                diagonal_counter += 1
                if diagonal_counter == self.s-1:
                    return current_state_flipped[i][i]
            else:
                diagonal_counter = 0
        if (self.n > self.s):  # check for a win on the remaining diagonals
            diagonal1_counter = 0
            diagonal2_counter = 0
            for i in range(1, self.n-self.s):
                for j in range(1, self.n-i):
                    if (current_state_flipped[j-1][i+j-1] != '.' and current_state_flipped[j-1][i+j-1] != 'b' and current_state_flipped[j-1][i+j-1] == current_state_flipped[j][i+j]):
                        diagonal1_counter += 1

                        if diagonal_counter == self.s-1:
                            return current_state_flipped[j][i+j]
                    else:
                        diagonal2_counter = 0

                    if (current_state_flipped[i+j-1][j-1] != '.' and current_state_flipped[i+j-1][j-1] != 'b' and current_state_flipped[i+j-1][j-1] == current_state_flipped[i+j][j]):
                        diagonal2_counter += 1

                        if diagonal_counter == self.s-1:
                            return current_state_flipped[i][i+j]
                    else:
                        diagonal2_counter = 0
                diagonal1_counter = 0
                diagonal2_counter = 0

        # Is whole board full?
        for i in range(0, self.n):
            for j in range(0, self.n):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == '.'):
                    return None
        # It's a tie!
        return '.'

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == '◦':
                print('The winner is ◦!')
            elif self.result == '•':
                print('The winner is •!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == '◦':
            self.player_turn = '•'
        elif self.player_turn == '•':
            self.player_turn = '◦'
        return self.player_turn

    def minimax(self, max=False):
        # Minimizing for '•' and maximizing for '◦'
        # Possible values are:
        # -1 - win for '•'
        # 0  - a tie
        # 1  - loss for '•'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == '•':
            return (-1, x, y)
        elif result == '◦':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = '◦'
                        (v, _, _) = self.minimax(max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = '•'
                        (v, _, _) = self.minimax(max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    def alphabeta(self, alpha=-2, beta=2, max=False):
        # Minimizing for '•' and maximizing for '◦'
        # Possible values are:
        # -1 - win for '•'
        # 0  - a tie
        # 1  - loss for '•'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == '•':
            return (-1, x, y)
        elif result == '◦':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, self.n):
            for j in range(0, self.n-3):
                # print(self.current_state[i][j])
                # print(self.current_state)
                # print('◦' == '◦')
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = '◦'
                        (v, _, _) = self.alphabeta(alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = '•'
                        (v, _, _) = self.alphabeta(alpha, beta, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value
        return (value, x, y)

    def play(self, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        # if player_x == None:
        #     player_x = self.HUMAN
        # if player_o == None:
        #     player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == '◦':
                    (_, x, y) = self.minimax(max=False)
                else:
                    (_, x, y) = self.minimax(max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == '◦':
                    (m, x, y) = self.alphabeta(max=False)
                    print('Min')
                    print((m, x, y))
                else:
                    (m, x, y) = self.alphabeta(max=True)
                    print('Max')
                    print((m, x, y))

            end = time.time()
            if (self.player_turn == '◦' and player_x == self.HUMAN) or (self.player_turn == '•' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == '◦' and player_x == self.AI) or (self.player_turn == '•' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(
                    F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            
            self.current_state[x][y] = self.player_turn
            self.switch_player()

    # New Heuristic - now the slower one

# This heuristic calculates the total possible wins the first player can have and subtracts it from the total possible wins
# the second player can have. In counts how close each player is to completing a win and adds it to their total possible wins

    def sophisticated_heuristic(self):

        # Available wins for player 1 and player 2
        avail_p1 = avail_p2 = 0
        board = np.array(self.current_state)

    # Returns the board as a boolean ndarray where the true values are assigned to the empty position as well as the respective players
    # symbols on the board
        board_p1 = (board == '.') | (board == 'X')
        board_p2 = (board == '.') | (board == 'O')

    # Overlapping sub arrays of the board with their lengths the size of the win conditions
        horizontal_blocs_p1 = np.lib.stride_tricks.sliding_window_view(
            board_p1, (1, 3)).reshape(-1, 3)
        vertical_blocs_p1 = np.lib.stride_tricks.sliding_window_view(
            board_p1, (3, 1)).reshape(-1, 3)
        diagonal_blocs_p1 = np.lib.stride_tricks.sliding_window_view(
            board_p1, (3, 3)).reshape(-1, 3, 3)

        horizontal_blocs_p2 = np.lib.stride_tricks.sliding_window_view(
            board_p2, (1, 3)).reshape(-1, 3)
        vertical_blocs_p2 = np.lib.stride_tricks.sliding_window_view(
            board_p2, (3, 1)).reshape(-1, 3)
        diagonal_blocs_p2 = np.lib.stride_tricks.sliding_window_view(
            board_p2, (3, 3)).reshape(-1, 3, 3)

    # seperates the player's positions and empty positions - Used later to count how close each player is to a win
        horizontal_prog = (horizontal_blocs_p1+1) - (horizontal_blocs_p2+1)
        vertical_prog = (vertical_blocs_p1+1) - (vertical_blocs_p2+1)

    # Iterates through the overlapping sub arrays containing the vertical and horizontal positions and calculates their total score
        for i in range(len(horizontal_blocs_p1)):
            if horizontal_blocs_p1[i].all():
                avail_p1 += 1
                avail_p1 += np.count_nonzero(horizontal_prog[i] == 1) ** 2
            if vertical_blocs_p1[i].all():
                avail_p1 += 1
                avail_p1 += np.count_nonzero(vertical_prog[i] == 1) ** 2

            if horizontal_blocs_p2[i].all():
                avail_p2 += 1
                avail_p2 += np.count_nonzero(horizontal_prog[i] == -1) ** 2

            if vertical_blocs_p2[i].all():
                avail_p2 += 1
                avail_p2 += np.count_nonzero(vertical_prog[i] == -1) ** 2

    # Iterates through the overlapping sub arrays containing the diagonal positions and calculates their total score
        for s in range(len(diagonal_blocs_p1)):

            # nw = north-west, ne = north-east
            nw_p1 = np.diagonal(diagonal_blocs_p1[s])
            ne_p1 = np.diagonal(np.fliplr(diagonal_blocs_p1[s]))

            nw_p2 = np.diagonal(diagonal_blocs_p2[s])
            ne_p2 = np.diagonal(np.fliplr(diagonal_blocs_p2[s]))

            diagonal_prog_nw = (nw_p1+1) - (nw_p2+1)
            diagonal_prog_ne = (ne_p1+1) - (ne_p2+1)

            if nw_p1.all():
                avail_p1 += 1
                avail_p1 += np.count_nonzero(diagonal_prog_nw == 1) ** 2

            if ne_p1.all():
                avail_p1 += 1
                avail_p1 += np.count_nonzero(diagonal_prog_ne == 1) ** 2

            if nw_p2.all():
                avail_p2 += 1
                avail_p2 += np.count_nonzero(diagonal_prog_nw == -1) ** 2

            if ne_p2.all():
                avail_p2 += 1
                avail_p2 += np.count_nonzero(diagonal_prog_ne == -1) ** 2

        return avail_p1 - avail_p2

    # Max player will always be the white pieces since that player always goes first.

    def slow_heuristic(self):
        start = time.time()
        # Matrix of zeros used to evaluate the max player's score for each of its pieces.
        max_matrix = np.zeros((self.n, self.n))
        # Matrix of zeros used to evaluate the min player's score for each of its pieces.
        min_matrix = np.zeros((self.n, self.n))
        # Boolean matrix to indentify the white pieces.
        white_matrix = np.zeros((self.n, self.n), dtype=bool)
        # Boolean matrix to indentify the black pieces.
        black_matrix = np.zeros((self.n, self.n), dtype=bool)
        # Matrix for max used to store the sum of adjacent values.
        max_score_matrix = np.zeros((self.n, self.n))
        # Matrix for min used to store the sum of adjacent values.
        min_score_matrix = np.zeros((self.n, self.n))
        # Matrix used to store the final score of the pieces of max.
        max_final_score_matrix = np.zeros((self.n, self.n))
        # Matrix used to store the final score of the pieces of max.
        min_final_score_matrix = np.zeros((self.n, self.n))

        # Loop that will go through each position of the current state and perform the heuristic.
        for i in range(0, self.n):
            for j in range(0, self.n):
                # Each box is worth 0 points.
                if (self.current_state[i][j] == 'b'):
                    max_matrix[i, j] = 0
                    min_matrix[i, j] = 0
                # Each empty position is worth 1 for the max player and -1 for the min player.
                elif (self.current_state[i][j] == '.'):
                    max_matrix[i, j] = 1
                    min_matrix[i, j] = -1
                # Each white piece is worth 2 points.
                elif (self.current_state[i][j] == '◦'):
                    max_matrix[i, j] = 2
                    min_matrix[i, j] = 2
                    white_matrix[i, j] = True
                # Each black piece is worth -2 points.
                elif (self.current_state[i][j] == '•'):
                    max_matrix[i, j] = -2
                    min_matrix[i, j] = -2
                    black_matrix[i, j] = True
        # Loop that will set the values of the pieces to the sum of the adjacent values.
        for i in range(0, self.n):
            for j in range(0, self.n):
                max_region = max_matrix[max(0, i-1): i+2,
                                        max(0, j-1): j+2]
                max_score_matrix[i, j] = np.sum(max_region) - max_matrix[i, j]
                min_region = min_matrix[max(0, i-1): i+2,
                                        max(0, j-1): j+2]
                min_score_matrix[i, j] = np.sum(min_region) - min_matrix[i, j]
        max_final_score_matrix = np.where(white_matrix, max_score_matrix, 0)
        min_final_score_matrix = np.where(black_matrix, min_score_matrix, 0)
        end = time.time()
        print(end - start)
        # Returns the sum of the all the scores in both max and min score matrices.
        return np.sum(max_final_score_matrix) + np.sum(min_final_score_matrix)

# Class used to test my heurisic while we build the functional game class.


class Test_case:
    def __init__(self, n=5, current_state=[['b', '.', '•', '.', '.'],
                                           ['.', '•', '◦', 'b', '.'],
                                           ['.', 'b', '◦', '.', '.'],
                                           ['.', '.', '◦', 'b', '.'],
                                           ['.', '.', '•', '.', '.']]):
        self.n = n
        self.current_state = current_state

    def slow_heuristic(self):
        start = time.time()
        # Matrix of zeros used to evaluate the max player's score for each of its pieces.
        max_matrix = np.zeros((self.n, self.n))
        # Matrix of zeros used to evaluate the min player's score for each of its pieces.
        min_matrix = np.zeros((self.n, self.n))
        # Boolean matrix to indentify the white pieces.
        white_matrix = np.zeros((self.n, self.n), dtype=bool)
        # Boolean matrix to indentify the black pieces.
        black_matrix = np.zeros((self.n, self.n), dtype=bool)
        # Matrix for max used to store the sum of adjacent values.
        max_score_matrix = np.zeros((self.n, self.n))
        # Matrix for min used to store the sum of adjacent values.
        min_score_matrix = np.zeros((self.n, self.n))
        # Matrix used to store the final score of the pieces of max.
        max_final_score_matrix = np.zeros((self.n, self.n))
        # Matrix used to store the final score of the pieces of max.
        min_final_score_matrix = np.zeros((self.n, self.n))

        # Loop that will go through each position of the current state and perform the heuristic.
        for i in range(0, self.n):
            for j in range(0, self.n):
                # Each box is worth 0 points.
                if (self.current_state[i][j] == 'b'):
                    max_matrix[i, j] = 0
                    min_matrix[i, j] = 0
                # Each empty position is worth 1 for the max player and -1 for the min player.
                elif (self.current_state[i][j] == '.'):
                    max_matrix[i, j] = 1
                    min_matrix[i, j] = -1
                # Each white piece is worth 2 points.
                elif (self.current_state[i][j] == '◦'):
                    max_matrix[i, j] = 2
                    min_matrix[i, j] = 2
                    white_matrix[i, j] = True
                # Each black piece is worth -2 points.
                elif (self.current_state[i][j] == '•'):
                    max_matrix[i, j] = -2
                    min_matrix[i, j] = -2
                    black_matrix[i, j] = True
        # print("MAX_MATRIX")
        # print(max_matrix)
        # print("WHITE_MATRIX")
        # print(white_matrix)
        # print("MIN_MATRIX")
        # print(min_matrix)
        # print("BLACK_MATRIX")
        # print(black_matrix)
        # Loop that will set the values of the pieces to the sum of the adjacent values.
        for i in range(0, self.n):
            for j in range(0, self.n):
                max_region = max_matrix[max(0, i-1): i+2,
                                        max(0, j-1): j+2]
                max_score_matrix[i, j] = np.sum(max_region) - max_matrix[i, j]
                min_region = min_matrix[max(0, i-1): i+2,
                                        max(0, j-1): j+2]
                min_score_matrix[i, j] = np.sum(min_region) - min_matrix[i, j]
        # print("MAX_SCORE_MATRIX")
        # print(max_score_matrix)
        # print("MIN_SCORE_MATRIX")
        # print(min_score_matrix)
        max_final_score_matrix = np.where(white_matrix, max_score_matrix, 0)
        min_final_score_matrix = np.where(black_matrix, min_score_matrix, 0)
        # print("MAX_FINAL_SCORE_MATRIX")
        # print(max_final_score_matrix)
        # print("MIN_FINAL_SCORE_MATRIX")
        # print(min_final_score_matrix)
        end = time.time()
        print(end - start)
        # Returns the sum of the all the scores in both max and min score matrices.
        return np.sum(max_final_score_matrix) + np.sum(min_final_score_matrix)


def main():
    # n, b, s, coordinates_list, d1, d2, t, a, play_mode = input_extraction()
    g = Game(5, 4, 4, [(0, 0), (1, 3), (2, 1), (3, 3)],
             1, 1, 5, False, 4, recommend=True)
    g.draw_board()
    # case = Test_case()
    # print(case.slow_heuristic())
    g.play()
    # g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)


if __name__ == "__main__":
    main()
