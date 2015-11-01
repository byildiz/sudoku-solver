#!/usr/bin/python

"""
Sudoko is one of the most famous Constraint Satisfaction Problem (CPS)

In this code, a given Sudoko problem solved using backtracking method
by searching depth-first-search.

See sudoku.txt for example input
Example sudoku is from "Sudoku Ileri Seviye 9" by Okan Arikan and Sinan Cecen

Example usage: python solver.py sudoko.txt

Author: Burak YILDIZ (yildiz1088 [a] gmail [.] com)
"""

import sys, copy

class State:
	def __init__(self, prev_state):
		self.rows = [[]]*9
		self.cols = [[]]*9
		self.squs = [[[]]*3 for i in range(3)]
		self.cans = []
		if prev_state != None:
			self.board = copy.deepcopy(prev_state.board)
			self.depth = prev_state.depth + 1
		else:
			self.board = [[0]*9 for i in  range(9)]
			self.depth = 0

def main(argv):
	if len(argv) != 2:
		print "Usage: {} <input_file>".format(argv[0])
		exit(1)
	input_file = open(argv[1], 'r')
	start_state = State(None)
	for i in range(9):
		line = input_file.readline()
		row = line.split()
		for j in range(9):
			start_state.board[i][j] = int(row[j])
	
	print "Sudoku:"
	print_board(start_state.board)
	solved, end_state = solve(start_state)
	if solved:
		print "Solution:"
		print_board(end_state.board)
	else:
		print "There is no valid combination for this sudoku"
	
def solve(state):
	print "Depth: {}".format(state.depth)
	# find filled for each row col and square
	find_filled(state)
	for i in range(9):
		for j in range(9):
			# already filled?
			if not state.board[i][j]:
				candidates = []
				for x in range(1, 10):
					if not (x in state.rows[i] or x in state.cols[j] or x in state.squs[i/3][j/3]):
						candidates.append(x);
				# if there is just one possible candidate, fill it
				if len(candidates) == 1:
					state.board[i][j] = candidates[0]
				else:
					state.cans.append(((i, j), candidates))
	# refill because of the new filled box
	find_filled(state)
	# search a conflict
	if is_error(state):
		return False, state
	# test whether it is solved
	if is_solved(state):
		return True, state
	# try the fill all possible candidates starting with the box has least possible number of candidates
	state.cans = sorted(state.cans, key=lambda x: len(x[1]))
	if len(state.cans) > 0:
		box, candidates = state.cans[0]
		for candidate in candidates:
			print "Try to fill box {} with {}".format(box, candidate)
			next_state = State(state)
			next_state.board[box[0]][box[1]] = candidate
			solved, end_state = solve(next_state)
			if solved:
				return True, end_state
	# not solvable sudoku
	return False, state

def print_board(board):
	for i in range(9):
		if i%3 == 0:
			print "-------------------------"
		for j in range(9):
			if j%3 == 0:
				print "|",
			print " " if board[i][j] == 0 else board[i][j],
		print "|"
	print "-------------------------"

def find_filled(state):
	# founds must be ordered for error detection in is_error
	for i in range(9):
		# find found in row
		state.rows[i] = sorted([x for x in state.board[i] if x != 0])
		# find found in col
		state.cols[i] = sorted([state.board[j][i] for j in range(9) if state.board[j][i] != 0])

	# find found in square
	for i in range(3):
		for j in range(3):
			state.squs[i][j] = []
			for r in state.board[(i*3):(i*3)+3]:
				state.squs[i][j] += [x for x in r[(j*3):(j*3)+3] if x != 0]
			state.squs[i][j] = sorted(state.squs[i][j])

def is_error(state):
	for i in range(9):
		for j in range(1, len(state.rows[i])):
			if state.rows[i][j-1] == state.rows[i][j]:
				# print "Error in row %d" % i
				return True
		for j in range(1, len(state.cols[i])):
			if state.cols[i][j-1] == state.cols[i][j]:
				# print "Error in col %d" % i
				return True
	for i in range(3):
		for j in range(3):
			for k in range(1, len(state.squs[i][j])):
				if state.squs[i][j][k-1] == state.squs[i][j][k]:
					# print "Error in square %d, %d" % i, j 
					return True
	return False

def is_solved(state):
	for i in range(9):
		if len(state.rows[i]) != 9:
			return False
	return True

if __name__ == '__main__':
	main(sys.argv)