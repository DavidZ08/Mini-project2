#New Heuristic - now the slower one
import numpy as np
## This heuristic calculates the total possible wins the first player can have and subtracts it from the total possible wins 
## the second player can have. In counts how close each player is to completing a win and adds it to their total possible wins

def sophisticated_heuristic(self):

        # Available wins for player 1 and player 2
        avail_p1 = avail_p2 = 0
        board = np.array(self.current_state)

        # Returns the board as a boolean ndarray where the true values are assigned to the empty position as well as the respective players
        # symbols on the board
        board_p1 = (board == '.') | (board == 'X')
        board_p2 = (board == '.') | (board == 'O')

        # Overlapping sub arrays of the board with their lengths the size of the win conditions
        horizontal_blocs_p1 = np.lib.stride_tricks.sliding_window_view(board_p1, (1, 3)).reshape(-1, 3)
        vertical_blocs_p1 = np.lib.stride_tricks.sliding_window_view(board_p1, (3, 1)).reshape(-1, 3)
        diagonal_blocs_p1 = np.lib.stride_tricks.sliding_window_view(board_p1, (3, 3)).reshape(-1, 3, 3)

        horizontal_blocs_p2 = np.lib.stride_tricks.sliding_window_view(board_p2, (1, 3)).reshape(-1, 3)
        vertical_blocs_p2 = np.lib.stride_tricks.sliding_window_view(board_p2, (3, 1)).reshape(-1, 3)
        diagonal_blocs_p2 = np.lib.stride_tricks.sliding_window_view(board_p2, (3, 3)).reshape(-1, 3, 3)

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
