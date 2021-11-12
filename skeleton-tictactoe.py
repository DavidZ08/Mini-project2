# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import sys

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

def boolean_extraction(question, bound1, bound2):
	user_input = int_extraction(question, bound1, bound2)
	if (user_input == 1):
		return False
	else:
		return True

def blocposition_extraction(board_size, bloc_number):
	coordinates_list = list()
	x_pos = 0
	y_pos = 0
	for i in range(bloc_number):
		while not int(x_pos) in range (0, board_size):
			print("Enter the x coordinate of your bloc.")
			x_pos_string = input()
			x_pos = coordinate_extraction(x_pos_string)
		while not int(y_pos) in range (0, board_size):
			print("Enter the y coordinate of your bloc.")
			y_pos = input()
		coordinate_tuple = (x_pos, y_pos)
		coordinates_list.append(coordinate_tuple)
	return coordinates_list

def input_extraction():
	n = int_extraction("Please enter the size of the board [3, 10]", 3, 10)
	b = int_extraction("Please enter the number of blocs [2, 2*sizeofboard]", 3, 2*n)
	s = int_extraction("Please enter the winning line-up size [3, sizeofboard]", 3, n)
	coordinates_list = blocposition_extraction(n-1, b)
	d1 = int_extraction("Please enter the maximum depth of the adverserial search d1 [1, sizeofboard]", 1, n-1)
	d2 = int_extraction("Please enter the maximum depth of the adverserial search d2 [1, sizeofboard]", 1, n-1)
	t = int_extraction("Please enter the maximum allowed time for the program to return a move", 1, float('inf'))
	a = boolean_extraction("To force the use of minimax, enter '1'. To force the use of alphabeta, enter '2'", 1, 2)
	play_mode = int_extraction("Please enter the game mode: 1. H-H, 2. H-AI, 3. AI-H, 4. AI-AI", 1, 4)
	return n, b, coordinates_list, d1, d2, t, a, play_mode

def coordinate_extraction(str):
	alphabet_coordinates = {'A': 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'H' : 6, 'I' : 7, 'J' : 8, 'K' : 9}
	return alphabet_coordinates[str]

def move_extraction_human(board_size):
	#TODO: finish this method for human players, gives them only one chance to re-enter their move. In case of another failure, makes player lose the game.
	print("Enter the x coordinate of your move.")
	x_pos_string = input()
	x_pos = coordinate_extraction(x_pos_string)
	if (x_pos > board_size or x_pos < 0):
		print("Enter the y coordinate of your move.")
	y_pos = input()
	coordinate_tuple = (x_pos, y_pos)
	return coordinate_tuple

#TODO: Finish method for AI players, gives them 0 chances.
class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	n = 0
	b = 0;
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
		# Player ◦ always plays first
		self.player_turn = '◦'

	def draw_board(self):
		print()
		for y in range(0, self.n):
			for x in range(0, self.n):
				print(F'{self.current_state[x][y]}', end="")
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
			for j in range (1, self.n):
				if (self.current_state[i][j-1] != '.' and self.current_state[i][j-1] == self.current_state[i][j]):
					vertical_counter += 1
					if vertical_counter == self.s-1:
						return self.current_state[i][j]
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
				if (self.current_state[j-1][i] != '.' and self.current_state[j-1][i] == self.current_state[j][i]):
					horizontal_counter += 1
					if horizontal_counter == self.s-1:
						return self.current_state[j][i]
					else:
						continue
				else:
					horizontal_counter = 0
					continue
			horizontal_counter = 0

		# Main diagonal win
		if (self.current_state[0][0] != '.' and
			self.current_state[0][0] == self.current_state[1][1] and
			self.current_state[0][0] == self.current_state[2][2]):
			return self.current_state[0][0]
		# Second diagonal win
		if (self.current_state[0][2] != '.' and
			self.current_state[0][2] == self.current_state[1][1] and
			self.current_state[0][2] == self.current_state[2][0]):
			return self.current_state[0][2]
			
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
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == '◦':
			self.player_turn = '•'
		elif self.player_turn == '•':
			self.player_turn = '◦'
		return self.player_turn

	def minimax(self, max=False):
		# Minimizing for '◦' and maximizing for '•'
		# Possible values are:
		# -1 - win for '◦'
		# 0  - a tie
		# 1  - loss for '◦'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == '◦':
			return (-1, x, y)
		elif result == '•':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.n):
			for j in range(0, self.n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = '•'
						(v, _, _) = self.minimax(max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = '◦'
						(v, _, _) = self.minimax(max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for '◦' and maximizing for '•'
		# Possible values are:
		# -1 - win for '◦'
		# 0  - a tie
		# 1  - loss for '◦'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == '◦':
			return (-1, x, y)
		elif result == '•':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.n):
			for j in range(0, self.n):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = '•'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = '◦'
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

	def play(self,algo=None,player_x=None,player_o=None):
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
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
			else: # algo == self.ALPHABETA
				if self.player_turn == '◦':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == '◦' and player_x == self.HUMAN) or (self.player_turn == '•' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == '◦' and player_x == self.AI) or (self.player_turn == '•' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.current_state[x][y] = self.player_turn
			self.switch_player()

def main():
	# n, b, s, coordinates_list, d1, d2, t, a, play_mode = input_extraction()
	g = Game(4, 0, 4, list(), 0, 0, 0, True, 1,recommend=True)
	g.draw_board()
	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()

