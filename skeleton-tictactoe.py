# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import sys
import numpy as np


def int_extraction(question, bound1, bound2):							#Method that will be used to prompt the user for an integer and check that it is within bounds.
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

def boolean_extraction(question, bound1, bound2):						#Method that will prompt the user for a boolean.
	user_input = int_extraction(question, bound1, bound2)
	if (user_input == 0):
		return False
	else:
		return True

def blocposition_extraction(board_size, bloc_number):					#Method that will prompt the user for the positions of the blocs.
	alphabet_coordinates = {'A': 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G': 6, 'H' : 7, 'I' : 8, 'J' : 9, 'K' : 10, 'L' : 11, 'M' : 12, 'B' : 13, 'O' : 14, 'P' : 15, 'Q' : 16,
	 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V' : 21, 'W' : 22, 'X': 23, 'Y': 24, 'Z': 25}
	coordinates_list = list()
	x_pos = 0
	x_pos_string = "A"
	y_pos = 0
	for i in range(bloc_number):
		print("Enter the x coordinate of your bloc.")
		x_pos_string = input()	
		while x_pos_string not in alphabet_coordinates.keys() or not alphabet_coordinates[x_pos_string] in range(0, board_size):
			print("Enter the x coordinate of your bloc.")
			x_pos_string = input()	
		print("Enter the y coordinate of your bloc.")
		y_pos = input()
		while not int(y_pos) in range (0, board_size):
			print("Enter the y coordinate of your bloc.")
			y_pos = input()
		y_pos = int(y_pos)
		coordinate_tuple = (y_pos, x_pos)
		coordinates_list.append(coordinate_tuple)
	return coordinates_list

def blocposition_extraction(board_size, bloc_number):					#Method that will prompt the user for the positions of the move.
	alphabet_coordinates = {'A': 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G': 6, 'H' : 7, 'I' : 8, 'J' : 9, 'K' : 10, 'L' : 11, 'M' : 12, 'B' : 13, 'O' : 14, 'P' : 15, 'Q' : 16,
	 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V' : 21, 'W' : 22, 'X': 23, 'Y': 24, 'Z': 25}
	x_pos = 0
	x_pos_string = "A"
	y_pos = 0
	for i in range(bloc_number):
		print("Enter the column (A... nth letter).")
		x_pos_string = input()	
		if x_pos_string not in alphabet_coordinates.keys() or not alphabet_coordinates[x_pos_string] in range(0, board_size):
			print("Enter the column of your move (A... nth letter).")
			x_pos_string = input()
		print("Enter the row of your move (0...n-1).")
		y_pos = input()
		if not int(y_pos) in range (0, board_size):
			print("Enter the row of your move (0...n-1).")
			y_pos = input()
		y_pos = int(y_pos)
		coordinate_tuple = (y_pos, x_pos) 
	return coordinate_tuple

def input_extraction():																#Method that will be used to prompt the user for the various parameters needed to initiate a game.
	n = int_extraction("Please enter the size of the board [3, 10]", 3, 10)
	b = int_extraction("Please enter the number of blocs [2, 2*sizeofboard]", 3, 2*n)
	s = int_extraction("Please enter the winning line-up size [3, sizeofboard]", 3, n)
	coordinates_list = blocposition_extraction(n, b)
	d1 = int_extraction("Please enter the maximum depth of the adverserial search d1 [1, sizeofboard]", 1, n-1)
	d2 = int_extraction("Please enter the maximum depth of the adverserial search d2 [1, sizeofboard]", 1, n-1)
	t = int_extraction("Please enter the maximum allowed time for the program to return a move", 1, float('inf'))
	a = boolean_extraction("To force the use of minimax, enter '0'. To force the use of alphabeta, enter '1'", 0, 1)
	play_mode = int_extraction("Please enter the game mode: 1. H-H, 2. H-AI, 3. AI-H, 4. AI-AI", 1, 4)
	return n, b, s, coordinates_list, d1, d2, t, a, play_mode

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
		alphabet_coordinates = {'A': 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G': 6, 'H' : 7, 'I' : 8, 'J' : 9, 'K' : 10, 'L' : 11, 'M' : 12, 'B' : 13, 'O' : 14, 'P' : 15, 'Q' : 16,
	 		'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V' : 21, 'W' : 22, 'X': 23, 'Y': 24, 'Z': 25}
		px = alphabet_coordinates[px]
		py = int(py)
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
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			self.initialize_game()
		return self.result

	def input_move(self):
		alphabet_coordinates = {'A': 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G': 6, 'H' : 7, 'I' : 8, 'J' : 9, 'K' : 10, 'L' : 11, 'M' : 12, 'B' : 13, 'O' : 14, 'P' : 15, 'Q' : 16,
	 		'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V' : 21, 'W' : 22, 'X': 23, 'Y': 24, 'Z': 25}
		attempt_counter = 0
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = input('Enter the column (A... nth letter) of the move.')
			py = int(input('Enter the row of your move (0...n-1) of the move.'))
			if self.is_valid(px, py):
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

	def minimax(self, start_time, max_depth, depth, max=False):
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
			return (self.slow_heuristic(), x, y)
		if time.time() - start_time + 0.20 >= self.t:
			return (self.slow_heuristic(), x, y)
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
						(v, _, _) = self.minimax(start_time, max_depth, depth, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(start_time, max_depth, depth, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, start_time, max_depth, depth, alpha=-2, beta=2, max=False):
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
			return (self.slow_heuristic(), x, y)
		if time.time() - start_time + 0.20 >= self.t:
			return (self.slow_heuristic(), x, y)
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
						(v, _, _) = self.alphabeta(start_time, max_depth, depth, alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(start_time, max_depth, depth, alpha, beta, max=True)
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
		if algo == None:

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
					(_, x, y) = self.minimax(start_time=start, max=False, max_depth=self.d2, depth=-1)
				else:
					(_, x, y) = self.minimax(start_time=start, max=True, max_depth=self.d1, depth=-1)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(start_time=start, max=False, max_depth=self.d2, depth=-1)
				else:
					(m, x, y) = self.alphabeta(start_time=start, max=True, max_depth=self.d1, depth=-1)
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
		
#Class used to test my heurisic while we build the functional game class.		
class Test_case:
	def __init__(self, n = 5, current_state = [['B', '.', 'X', '.', '.'],
				 							   ['.', 'X', 'O', 'B', '.'],
				 							   ['.', 'B', 'O', '.', '.'],
				 							   ['.', '.', 'O', 'B', '.'],
				 							   ['.', '.', 'X', '.', '.']]):
		self.n = n
		self.current_state = current_state
	def slow_heuristic(self):
		start = time.time()
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
		# print("MAX_MATRIX")
		# print(max_matrix)
		# print("WHITE_MATRIX")
		# print(white_matrix)
		# print("MIN_MATRIX")
		# print(min_matrix)
		# print("BLACK_MATRIX")
		# print(black_matrix)
		for i in range(0, self.n):										#Loop that will set the values of the pieces to the sum of the adjacent values.
			for j in range(0, self.n):
				max_region = max_matrix[max(0, i-1) : i+2,
                    					max(0, j-1) : j+2]
				max_score_matrix[i, j] = np.sum(max_region) - max_matrix[i, j]
				min_region = min_matrix[max(0, i-1) : i+2,
                    					max(0, j-1) : j+2]
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
		return np.sum(max_final_score_matrix) + np.sum(min_final_score_matrix)		#Returns the sum of the all the scores in both max and min score matrices.
		
		
def main():
	# n, b, s, coordinates_list, d1, d2, t, a, play_mode = input_extraction()
	g = Game(5, 4, 4, [(0,0),(1,3),(2,1),(3,3)], 6, 6, 5, False, 3,recommend=True)
	# print(blocposition_extraction(5, 1))
	# g.draw_board()
	# case = Test_case()
	# print(case.slow_heuristic())	
	g.play()
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)

if __name__ == "__main__":
    main()
