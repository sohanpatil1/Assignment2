import random
import numpy as np
import time
import pygame
import math
import sys
from connect4 import connect4
from copy import deepcopy

coinsinboard = False
countcoins = 0
depth = 0
NUMOFROWS = 6
NUMOFCOLS = 7

#Check which player is playing : env.turnPlayer.position
#Check if game over : env.gameOver()
#Copy current gameboard : deepcopy(env)
#move is a list that contains column of the next move



class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		print("Using Human Input")
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]
		print("Done Human Input")

class human2(connect4Player):

	def play(self, env, move):
		print("Using HumanTxt Input")
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True
		print("Done HumanTxt Input")

class randomAI(connect4Player):	#env is the current state of the gameboard, Called every turn

	def play(self, env, move):	#move : Its only passing a list for the move that needs to be done next
		print("Using Random AI")
		possible = env.topPosition >= 0	#True : Space for coin False : No space for coin
		#EDITS
		toppositions = []
		toppositions.append(env.topPosition)
		print("top positions",toppositions)
		#Edits
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]	#randomly choose a column to play the next move and assign to move[:]. move[] stores the next move

class stupidAI(connect4Player):

	def play(self, env, move):
		print("Using Stupid AI with type(env) = ",type(env))
		possible = env.topPosition >= 0	#Contains an array of the possible columns to place the next move
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)		
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]
		print("Done with StupidAI")

class minimaxAI(connect4Player):

	def play(self, env, move):
		print("Started Minimax AI")
		newenv = deepcopy(env)
		print("Type of newenv in play minimax is: ",type(newenv))
		player = env.turnPlayer.position
		board = newenv.getBoard()	#original board
		# move[:],value = self.minimax(1,env,board,player,move)
		col,minimax_score = self.minimax(1,newenv,board,player,move,0)
		print("Placing coin at Column :",col)
		# self.simulateMove(env, move, value)	#Value == player. if in case there is a bug EDITS
		move[:] = [col]	#Selected a move for that particular player
		print("Done with Minimax AI")


	def terminalnode(self,env,player,col):	 #Tells whether its the end of the game
		print("Checking winner in terminal node")
		return env.gameOver(col,player)

	def changeplayer(self,player):
		print("Changing player")
		switch = {1:2,2:1}
		return switch[player]

	def simulateMove(self,env, col, player):
		env.board[env.topPosition[col]][col] = player	#Fill in player in board[row][col]
		env.topPosition[col] -= 1
		#env.history[0].append(col)	#Only in history not in deepcopy, hence used to simulate move

	def minimax(self,depth,env,board,player,move,col):	#Which path to take and set payoffs using evaluation. Call evaluation for terminal nodes
		print("Calling minimax for depth :",depth)
		global coinsinboard
		if not coinsinboard:	#No coin placed
			print("Placed Coin in middle row")
			coinsinboard = True
			return 3,0	#col = self.minimax(1,env,board,player,move,3) and 0 is TEMPORARY

		if((depth == 4)):
			print("Reached if case with depth and terminal node")
			if(depth == 4):
				print("Reached depth 3")
				env.board[env.topPosition[col]][col] = player	#Fill in player in board[row][col]
				env.topPosition[col] -= 1
				return self.evaluation(env,player,move)	
		
		if(player == 1):	#if the AI is used as player 1
			print("For player 1")
			maximum = -math.inf
			possible = env.topPosition >= 0
			for col in enumerate(possible):
				if(possible[col]):
					newenv = deepcopy(env)	#Produces a 2d array of the board copy
					self.simulateMove(newenv, col, player)
					print("Depth before calling minimax : depth: ",depth+1)
					temp, value = self.minimax(depth+1,newenv,board,self.changeplayer(player),move,col) #Value is what is used for comparison
					print("Value for player 1: ",value,"and depth: ",depth+1)
					if value > maximum:
						placementcol = col
						maximum = value
			#depth = 0
			return placementcol,maximum
		else: #if minimax AI is used as player 2
			print("For player 2")
			minimum = math.inf
			possible = env.topPosition >= 0
			for col in enumerate(possible):
				if(possible[col]):
					newenv = deepcopy(env)	#Produces a 2d array of the board copy
					self.simulateMove(newenv, col, player)
					temp,value = self.minimax(depth+1,newenv,board,self.changeplayer(player),move,col)
					print("Value for player 2: ",value)
					if value < minimum:
						placementcol = col
						minimum = value
			#depth = 0
			return placementcol,minimum
			
	def evaluation(self,env,player,move): #returns payoff by calculating how good our move is for their current move.
		#Issue arises when 0,0 _ 0,0. My algo will not see this as potential win because it sees it as 2 pairs. Need to add implementation for this.
		print("Evaluating current node...")
		print("Type of newenv in evaluation function : ",type(env))
		newenv = deepcopy(env)
		print("Type of newenv in evaluation function : ",type(newenv))
		len4count = self.lencount(4, newenv,move,player)
		len3count = self.lencount(3, newenv,move,player)
		len2count = self.lencount(2, newenv,move,player)
		opplen4count = self.lencount(4, newenv,move,self.changeplayer(player))
		opplen3count = self.lencount(3, newenv,move,self.changeplayer(player))
		opplen2count = self.lencount(2, newenv,move,self.changeplayer(player))
		print("4 Length Player : ",len4count)
		print("3 Length Player : ",len3count)
		print("2 Length Player : ",len2count)
		print("4 Length Player : ",opplen4count)
		print("3 Length Player : ",opplen3count)
		print("2 Length Player : ",opplen2count)
		result = len4count*1000 + len3count*100 + len2count*10 - (opplen4count*1000 + opplen3count*100 + opplen2count*10)
		if(player == 1):
			return result
		return -result

	
	def lencount(self,inarow,env,move,player):
		#Horizontal Solutions
		newenv = deepcopy(env)
		print("Type of newenv in lencount is : ",type(newenv))
		print("In Lencount with inarow: ",inarow)
		for s in range(NUMOFROWS):
			if env.board[move][s] == player:
				count += 1
			else:
				count = 0
			if count >= inarow:
				lencount = lencount+1	#How many of len4 exist, possible wins
				count=0
		#Vertical Solutions
		count = 0
		for s in range(NUMOFCOLS):
			if env.board[s,move] == player:
				count += 1
			else:
				count = 0
			if count >= inarow:
				lencount += 1	#How many of instance of that length exist exist, possible wins
				count=0
		#Left Diagonal
		for r in range(NUMOFROWS-inarow-1):
			for c in range(NUMOFCOLS-inarow-1):
				selection = [env.board[r+i,c+i] for i in range(inarow)]
				if(selection.count(player) >= inarow):
					lencount += 1
		#Right Diagonal
		for r in range(NUMOFROWS-inarow-1):
			for c in range(NUMOFCOLS-inarow-1):
				selection = [env.board[r+inarow-1-i,c+i] for i in range(inarow)]
				if(selection.count(player) >= inarow):
					lencount += 1
		print("Done with Lencount using inarow: ",inarow)
		return lencount


class alphaBetaAI(connect4Player):

	def play(self, env, move):
		print("Started alphabeta AI")
		newenv = deepcopy(env)
		player = env.turnPlayer.position
		board = newenv.getBoard()	#original board
		# move[:],value = self.minimax(1,env,board,player,move)
		alpha = -math.inf
		beta = math.inf
		col,minimax_score = self.minimax(1,newenv,board,player,move,0,alpha,beta)
		print("Placing coin at Column :",col)
		# self.simulateMove(env, move, value)	#Value == player. if in case there is a bug EDITS
		move[:] = [col]	#Selected a move for that particular player
		print("Done with alphabeta AI")

	def terminalnode(self,env,player,col):	 #Tells whether its the end of the game
		print("Checking winner in terminal node")
		return env.gameOver(col,player)

	def changeplayer(self,player):
		print("Changing player")
		switch = {1:2,2:1}
		return switch[player]

	def simulateMove(self,env, col, player):
		env.board[env.topPosition[col]][col] = player	#Fill in player in board[row][col]
		env.topPosition[col] -= 1
		#env.history[0].append(col)	#Only in history not in deepcopy, hence used to simulate move

	def minimax(self,depth,env,board,player,move,col,alpha,beta):	#Which path to take and set payoffs using evaluation. Call evaluation for terminal nodes
		print("Calling minimax for depth :",depth)
		global coinsinboard
		if not coinsinboard:	#No coin placed
			print("Placed Coin in middle row")
			coinsinboard = True
			return 3,0	#col = self.minimax(1,env,board,player,move,3) and 0 is TEMPORARY

		if((depth == 3)):
			print("Reached if case with depth and terminal node")
			if(depth == 3):
				print("Reached depth 3")
				env.board[env.topPosition[col]][col] = player	#Fill in player in board[row][col]
				env.topPosition[col] -= 1
				return self.evaluation(board,player,move)	
		
		if(player == 1):	#if the AI is used as player 1
			print("For player 1")
			maximum = -math.inf
			possible = env.topPosition >= 0
			for col in enumerate(possible):
				if(possible[col]):
					newenv = deepcopy(env)	#Produces a 2d array of the board copy
					self.simulateMove(newenv, col, player)
					print("Depth before calling minimax : depth: ",depth+1)
					temp, value = self.minimax(depth+1,newenv,board,self.changeplayer(player),move,col,alpha,beta) #Value is what is used for comparison
					print("Value for player 1: ",value,"and depth: ",depth+1)
					if value > maximum:
						placementcol = col
						maximum = value
					alpha = max(alpha,value)
					if alpha >= beta:
						break
			#depth = 0
			return placementcol,maximum
		else: #if minimax AI is used as player 2
			print("For player 2")
			minimum = math.inf
			possible = env.topPosition >= 0
			for col in enumerate(possible):
				if(possible[col]):
					newenv = deepcopy(env)	#Produces a 2d array of the board copy
					self.simulateMove(newenv, col, player)
					temp,value = self.minimax(depth+1,newenv,board,self.changeplayer(player),move,col,alpha,beta)
					print("Value for player 2: ",value)
					if value < minimum:
						placementcol = col
						minimum = value
					beta = min(beta, value)
					if(alpha >= beta):
						break
			#depth = 0
			return placementcol,minimum
			
	def evaluation(self,env,player,move): #returns payoff by calculating how good our move is for their current move.
		#Issue arises when 0,0 _ 0,0. My algo will not see this as potential win because it sees it as 2 pairs. Need to add implementation for this.
		print("Evaluating current node...")
		newenv = deepcopy(env)
		len4count = self.lencount(4, newenv,move,player)
		len3count = self.lencount(3, newenv,move,player)
		len2count = self.lencount(2, newenv,move,player)
		opplen4count = self.lencount(4, newenv,move,self.changeplayer(player))
		opplen3count = self.lencount(3, newenv,move,self.changeplayer(player))
		opplen2count = self.lencount(2, newenv,move,self.changeplayer(player))
		print("4 Length Player : ",len4count)
		print("3 Length Player : ",len3count)
		print("2 Length Player : ",len2count)
		print("4 Length Player : ",opplen4count)
		print("3 Length Player : ",opplen3count)
		print("2 Length Player : ",opplen2count)
		result = len4count*1000 + len3count*100 + len2count*10 - (opplen4count*1000 + opplen3count*100 + opplen2count*10)
		if(player == 1):
			return result
		return -result

	
	def lencount(self,inarow,env,move,player):
		#Horizontal Solutions
		newenv = deepcopy(env)
		for s in range(NUMOFROWS):
			if newenv.board[move,s] == player:
				count += 1
			else:
				count = 0
			if count >= inarow:
				lencount = lencount+1	#How many of len4 exist, possible wins
				count=0
		#Vertical Solutions
		count = 0
		for s in range(NUMOFCOLS):
			if newenv.board[s][move] == player:
				count += 1
			else:
				count = 0
			if count >= inarow:
				lencount += 1	#How many of instance of that length exist exist, possible wins
				count=0
		#Left Diagonal
		for r in range(NUMOFROWS-inarow-1):
			for c in range(NUMOFCOLS-inarow-1):
				selection = [newenv.board[r+i][c+i] for i in range(inarow)]
				if(selection.count(player) >= inarow):
					lencount += 1
		#Right Diagonal
		for r in range(NUMOFROWS-inarow-1):
			for c in range(NUMOFCOLS-inarow-1):
				selection = [newenv.board[r+inarow-1-i][c+i] for i in range(inarow)]
				if(selection.count(player) >= inarow):
					lencount += 1
		return lencount

	def successorfunction():
		listofvalues = {}	
		



SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)