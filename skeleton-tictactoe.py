# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import sys
import numpy as np

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
	slow_heuristic_wins = 0
	sophisiticated_heuristic_wins = 0

	def __init__(self, n, b, s, coordinates_list, d1, d2, t, a, play_mode, recommend = True):
		self.n, self.b, self.s, self.coordinates_list, self.d1, self.d2, self.t, self.a, self.play_mode = n, b, s, coordinates_list, d1, d2, t, a, play_mode
		self.initialize_game()
		self.recommend = recommend
	
	def initialize_game(self):
		self.current_state = [['.'for i in range (self.n)] for j in range(self.n)]
		for i in self.coordinates_list:
			self.current_state[i[0]][i[1]] = 'B'
		# Player O always plays first
		self.player_turn = 'O'

	def draw_board(self):
		print()
		for y in range(0, self.n):
			for x in range(0, self.n):
				print(F'{self.current_state[y][x]}', end="")
			print()
		print()
		
	def is_valid(self, px, py):
		if px < 0 or px > self.n-1 or py < 0 or py > self.n-1:		
			print("This move is out of bounds!")
			return False
		elif self.current_state[px][py] != '.':
			print("This position is already occupied!")
			return False
		else:
			return True

	def is_end(self):
		
		#Vertical win
		vertical_counter = 0
		for i in range(0, self.n):
			for j in range (1, self.n):
				if (self.current_state[j-1][i] != '.' and self.current_state[j-1][i] != 'B' and self.current_state[j-1][i] == self.current_state[j][i]):
					vertical_counter += 1
					if vertical_counter == self.s-1:
						return self.current_state[j][i]
					else:
						continue
				else:
					vertical_counter = 0
					continue
			vertical_counter = 0 # It has to check every column completely for a vertical win before moving on to check for a horizontal win
		
		# Horizontal win
		horizontal_counter = 0
		for i in range(0, self.n):
			for j in range (1, self.n):
				if (self.current_state[i][j-1] != '.' and self.current_state[i][j-1] != 'B' and self.current_state[i][j-1] == self.current_state[i][j]):
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
		#First set of diagonals from top left to bottom right
		for i in range(1, self.n):												#check for a win on the main diagonal
			if (self.current_state[i-1][i-1] != '.' and self.current_state[i-1][i-1] != 'B' and self.current_state[i-1][i-1] == self.current_state[i][i]):
				diagonal_counter += 1
				if diagonal_counter == self.s-1:
					return self.current_state[i][i]
			else:
				diagonal_counter = 0
		if (self.n > self.s):													#check for a win on the remaining diagonals
			diagonal1_counter = 0
			diagonal2_counter = 0
			for i in range(1, self.n-self.s):
				for j in range (1, self.n-i):
					if (self.current_state[j-1][i+j-1] != '.' and self.current_state[j-1][i+j-1] != 'B' and self.current_state[j-1][i+j-1] == self.current_state[j][i+j]):
						diagonal1_counter += 1
					
						if diagonal_counter == self.s-1:
							return self.current_state[j][i+j]
					else:
						diagonal2_counter = 0
					
					if (self.current_state[i+j-1][j-1] != '.' and self.current_state[i+j-1][j-1] != 'B' and self.current_state[i+j-1][j-1] == self.current_state[i+j][j]):
						diagonal2_counter += 1
					
						if diagonal_counter == self.s-1:
							return self.current_state[i][i+j]
					else:
						diagonal2_counter = 0
				diagonal1_counter = 0
				diagonal2_counter = 0

		# Second set of diagonals from top right to bottom left
		#Flip the matrix
		diagonal_counter = 0
		current_state_flipped = []
		for i in range(len(self.current_state)):
			current_state_flipped.append(self.current_state[i][::-1])
		
		for i in range(1, self.n):											#check for a win on the main diagonal
			if (current_state_flipped[i-1][i-1] != '.' and current_state_flipped[i-1][i-1] != 'B' and current_state_flipped[i-1][i-1] == current_state_flipped[i][i]):
				diagonal_counter += 1
				if diagonal_counter == self.s-1:
					return current_state_flipped[i][i]
			else:
				diagonal_counter = 0
		if (self.n > self.s):												#check for a win on the remaining diagonals
			diagonal1_counter = 0
			diagonal2_counter = 0
			for i in range(1, self.n-self.s):
				for j in range (1, self.n-i):
					if (current_state_flipped[j-1][i+j-1] != '.' and current_state_flipped[j-1][i+j-1] != 'B' and current_state_flipped[j-1][i+j-1] == current_state_flipped[j][i+j]):
						diagonal1_counter += 1
					
						if diagonal_counter == self.s-1:
							return current_state_flipped[j][i+j]
					else:
						diagonal2_counter = 0
					
					if (current_state_flipped[i+j-1][j-1] != '.' and current_state_flipped[i+j-1][j-1] != 'B' and current_state_flipped[i+j-1][j-1] == current_state_flipped[i+j][j] ):
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
			if self.result == 'X':
				self.sophisticated_heuristic_wins += 1
				print('The winner is X!')
			elif self.result == 'O':
				self.slower_heuristic_wins += 1
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			self.initialize_game()
		return self.result

	def input_move(self):
		alphabet_coordinates = {'A': 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G': 6, 'H' : 7, 'I' : 8, 'J' : 9, 'K' : 10, 'L' : 11, 'M' : 12, 'N' : 13, 'O' : 14, 'P' : 15, 'Q' : 16,
	 		'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V' : 21, 'W' : 22, 'X': 23, 'Y': 24, 'Z': 25}
		attempt_counter = 0
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = input('Enter the column (A... nth letter) of the move.')
			py = int(input('Enter the row of your move (0...n-1) of the move.'))
			if self.is_valid(py, alphabet_coordinates[px]):
				return (py, alphabet_coordinates[px])
			else:
				attempt_counter += 1
				if attempt_counter == 2:
					return False

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def minimax(self, player, start_time, max_depth, depth, max=True):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:

		value = 200
		if max:
			value = -200
		x = None
		y = None
		if depth == max_depth:
			if player == 'O':
				return (self.slow_heuristic(), x, y)
			else:
				return (self.sophisticated_heuristic(), x, y)
		if time.time() - start_time + 0.50 >= self.t:
			if player == 'O':
				return (self.slow_heuristic(), x, y)
			else:
				return (self.sophisticated_heuristic(), x, y)
		depth += 1
		result = self.is_end()
		if result == 'X':
			return (-100, x, y)
		elif result == 'O':
			return (100, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.n):
			for j in range(0, self.n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(player, start_time, max_depth, depth, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(player, start_time, max_depth, depth, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, player, start_time, max_depth, depth, alpha=-200, beta=200, max=True):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		depth += 1
		value = 200
		if max:
			value = -200
		x = None
		y = None
		if depth == max_depth:
			if player == 'O':
				return (self.slow_heuristic(), x, y)
			else:
				return (self.sophisticated_heuristic(), x, y)
		if time.time() - start_time + 0.50 >= self.t:
			if player == 'O':
				return (self.slow_heuristic(), x, y)
			else:
				return (self.sophisticated_heuristic(), x, y)
		depth += 1
		result = self.is_end()
		if result == 'X':
			return (-100, x, y)
		elif result == 'O':
			return (100, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.n):
			for j in range(0, self.n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(player, start_time, max_depth, depth, alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(player, start_time, max_depth, depth, alpha, beta, max=True)
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

	def play(self,algo=None,player_x=None,player_o=None):
		if self.a == True:
			algo = self.ALPHABETA
		elif self.a == False:
			algo = self.MINIMAX
		if self.play_mode == 1:
			player_x = self.HUMAN
			player_o = self.HUMAN
		elif self.play_mode == 2:
			player_x = self.HUMAN
			player_o = self.AI
		elif self.play_mode == 3:
			player_x = self.AI
			player_o = self.HUMAN
		elif self.play_mode == 4:
			player_x = self.AI
			player_o = self.AI
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(player = 'X', start_time=start, max=False, max_depth=self.d2, depth=-1)
				else:
					(_, x, y) = self.minimax(player = 'O', start_time=start, max=True, max_depth=self.d1, depth=-1)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(player = 'X', start_time=start, max=False, max_depth=self.d2, depth=-1)
				else:
					(m, x, y) = self.alphabeta(player = 'O', start_time=start, max=True, max_depth=self.d1, depth=-1)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN):
				if self.recommend:
					print(F'Evaluation time: {round(end - start, 7)}s')
					print(F'Recommended move: x = {x}, y = {y}')
				(x,y) = (0,0)
				placeholder = self.input_move() 
				if type(placeholder) == bool and self.player_turn == 'X':
					print("Player X loses because of illegal move")
					return
				else: 
					(x,y) = placeholder
			if (self.player_turn == 'O' and player_o == self.HUMAN):
				if self.recommend:
					print(F'Evaluation time: {round(end - start, 7)}s')
					print(F'Recommended move: x = {x}, y = {y}')
				(x,y) = (0,0)
				placeholder = self.input_move()
				if type(placeholder) == bool and self.player_turn == 'O':
					print("Player O loses because of illegal move")
					return
				else: 
					(x,y) = placeholder
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}') #prints immediately for AI player.
						if self.is_valid(x,y) == False and self.player_turn == 'X':
							print("Player X loses because of illegal move")
							return
						if self.player_turn == 'X' and (end - start) > self.t:
							print("Player X loses because he exceeded the time limit")
							return
						if (self.is_valid(x,y) == False) and self.player_turn == 'O':
							print("Player O loses because of illegal move")
							return
						if self.player_turn == 'O' and (end - start) > self.t:
							print("Player O loses because he exceeded the time limit")
							return
			self.current_state[x][y] = self.player_turn
			self.switch_player()

	#Max player will always be the white pieces since that player always goes first.
	def slow_heuristic(self):
		max_matrix = np.zeros((self.n,self.n))							#Matrix of zeros used to evaluate the max player's score for each of its pieces.
		min_matrix = np.zeros((self.n,self.n))							#Matrix of zeros used to evaluate the min player's score for each of its pieces.
		white_matrix = np.zeros((self.n,self.n), dtype=bool)			#Boolean matrix to indentify the white pieces.
		black_matrix = np.zeros((self.n,self.n), dtype=bool)			#Boolean matrix to indentify the black pieces.
		max_score_matrix = np.zeros((self.n,self.n))					#Matrix for max used to store the sum of adjacent values.
		min_score_matrix = np.zeros((self.n,self.n))					#Matrix for min used to store the sum of adjacent values.
		max_final_score_matrix = np.zeros((self.n,self.n))				#Matrix used to store the final score of the pieces of max.
		min_final_score_matrix = np.zeros((self.n,self.n))				#Matrix used to store the final score of the pieces of max.

		for i in range(0, self.n):										#Loop that will go through each position of the current state and perform the heuristic.
			for j in range(0, self.n):
				if (self.current_state[i][j] == 'B'):					#Each box is worth 0 points.
					max_matrix[i, j] = 0
					min_matrix[i, j] = 0
				elif (self.current_state[i][j] == '.'):					#Each empty position is worth 1 for the max player and -1 for the min player.
					max_matrix[i, j] = 1
					min_matrix[i, j] = -1
				elif (self.current_state[i][j] == 'O'):					#Each white piece is worth 2 points.
					max_matrix[i, j] = 2
					min_matrix[i, j] = 2
					white_matrix[i, j] = True
				elif (self.current_state[i][j] == 'X'):					#Each black piece is worth -2 points.
					max_matrix[i, j] = -2
					min_matrix[i ,j] = -2
					black_matrix[i, j] = True
		for i in range(0, self.n):										#Loop that will set the values of the pieces to the sum of the adjacent values.
			for j in range(0, self.n):
				max_region = max_matrix[max(0, i-1) : i+2,
                    					max(0, j-1) : j+2]
				max_score_matrix[i, j] = np.sum(max_region) - max_matrix[i, j]
				min_region = min_matrix[max(0, i-1) : i+2,
                    					max(0, j-1) : j+2]
				min_score_matrix[i, j] = np.sum(min_region) - min_matrix[i, j]
		max_final_score_matrix = np.where(white_matrix, max_score_matrix, 0)
		min_final_score_matrix = np.where(black_matrix, min_score_matrix, 0)
		return np.sum(max_final_score_matrix) + np.sum(min_final_score_matrix)		#Returns the sum of the all the scores in both max and min score matrices.

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
		
def scoreboard_write(game, r):
	score_file = open("scoreboard.txt", "a")
	score_file.write("1. Parameters of the game: \n")
	score_file.write("n = ")
	score_file.write(game.n)
	score_file.write("\t")
	score_file.write("b = ")
	score_file.write(game.b)
	score_file.write("\t")
	score_file.write("l = ")
	score_file.write(game.l)
	score_file.write("\t")
	score_file.write("t = ")
	score_file.write(game.t)
	score_file.write("\t \n")
	score_file.write("2. Parameters of each player: \n")
	score_file.write("Player_O: \n")
	score_file.write("d1 = ")
	score_file.write(game.d1)
	score_file.write("\t")
	if game.a == True:
		score_file.write("a1 = alpha-beta\t")
	elif game.a == False:
		score_file.write("a1 = minimax\t")
	score_file.write("heuritistic = slower_heuristic\n")
	score_file.write("Player_O: \n")
	score_file.write("d2 = ")
	score_file.write(game.d2)
	score_file.write("\t")
	if game.a == True:
		score_file.write("a2 = alpha-beta\t")
	elif game.a == False:
		score_file.write("a2 = minimax\t")
	score_file.write("heuritistic = sophisticated_heuristic\n")
	score_file.write("3. Number of games played: \n")
	score_file.write(2*r)
	score_file.write("\n")
	score_file.write("5. Statistics for each game played \n")
	for i in range(2*r):
		# game.play()
		print("placeholder")
		#TODO: append statistics for each game played (section 2.5.1) over 2*r
	score_file.write("4. The number and percentage of wins for each heuristic: \n")
	score_file.write("Slower_heuristic wins and percentage = ") # This can be done after the game has finished running 2*r times, as we'll accumulate wins each time the game is played in the instance "game".
	score_file.write(game.slower_heuristic_wins)
	score_file.write(", ")
	score_file.write(game.slower_heuristic_wins / (2*r))
	score_file.write("\n")
	score_file.write("Sophisticated_heuristic wins and percentage = ")
	score_file.write(game.sophisticated_heuristic_wins)
	score_file.write(", ")
	score_file.write(game.sophisticated_heuristic_wins / (2*r))
	score_file.write("\n")
	score_file.close()

def main():
	# g = Game(5, 4, 4, [(0,0),(1,3),(2,1),(3,3)], 6, 6, 5, False, 3,recommend=True)
	g1 = Game (4,4,3,[(0,0),(0,3),(3,0),(3,3)],6,6,5,False,4, recommend=True) #game-Trace-4435
	g2 = Game (4,4,3,[(0,0),(0,3),(3,0),(3,3)],6,6,1,True,4, recommend=True) #game-Trace-4431
	g3 = Game (5,4,4,[(0,1),(2,3),(3,0),(2,3)],2,6,1,True,4, recommend=True) #game-Trace-5441
	g4 = Game (5,4,4,[(0,2),(3,2),(4,0),(4,4)],6,6,5,True,4, recommend=True) #game-Trace-5445
	g5 = Game (8,5,5,[(5,1),(6,2),(7,0),(1,1)],2,6,1,True,4, recommend=True) #game-Trace-8551
	g6 = Game (8,5,5,[(5,4),(6,2),(7,0),(1,1)],2,6,5,True,4, recommend=True) #game-Trace-8555
	g7 = Game (8,6,5,[(5,4),(6,2),(7,0),(1,1)],6,6,1,True,4, recommend=True) #game-Trace-8651
	g8 = Game (8,6,5,[(5,4),(6,2),(7,0),(1,1)],6,6,5,True,4, recommend=True) #game-Trace-8655
	scoreboard_write(g1,5)
	scoreboard_write(g2,5)
	scoreboard_write(g3,5)
	scoreboard_write(g4,5)
	scoreboard_write(g5,5)
	scoreboard_write(g6,5)
	scoreboard_write(g7,5)
	scoreboard_write(g8,5)
	# print(blocposition_extraction(5, 1))
	# g.draw_board()
	# case = Test_case()
	# print(case.slow_heuristic())	
	# g.play()
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)

if __name__ == "__main__":
    main()
