#Author: Ishi Sood
import string
import copy
 
def LoadFromFile(filepath):
	with open(filepath, "r") as f:
		N = f.readline()
		N = int(N)
		puzzle = f.readlines()
		hasHole = False 
		puzzle = convertToInt(puzzle)

		for element in puzzle:
			if len(element) != N:
				print("invalid puzzle - length")
				return None
			if "*" in element:
				hasHole = True
			for x in element:
				if x != "*":
					if int(x) < 1 or int(x) > N**2 - 1:
						print("invalid puzzle val")
						return None
		if len(puzzle) != N or hasHole == False:
			print("invalid puzzle")
			return None
		#DebugPrint(puzzle)
		print(puzzle)
		return puzzle

def convertToInt(puzzle):
	puzzle2 = []
	for element in puzzle:
		elementA = element.split()
		puzzle2.append(elementA)
	return puzzle2
	
def ComputeNeighbors(state):
	N = len(state)
	starIndex = findStarIndex(state)
	row = starIndex[0]
	column = starIndex[1]
	allIndex = [[row-1, column], [row+1, column], [row, column+1], [row, column-1]]
	legalIndex = checkValid(allIndex, N)

	newStates = []
	for element in legalIndex:
		tempState = copy.deepcopy(state)
		x = buildNewState(tempState, [row, column], element)
		newStates.append(x)
		
	return newStates

def findStarIndex(state):
	for row in range(len(state)):
		for col in range(len(state)):
			if state[row][col] == "*":
				index = [row, col]
				return index

def buildNewState(state, star, newPositin):
	ogRow = star[0] 
	ogCol = star[1]
	newRow = newPositin[0]
	newCol = newPositin[1]

	newChar = state[newRow][newCol]
	state[ogRow][ogCol] = newChar
	state[newRow][newCol] = "*"

	newstate = (newChar, state)
	return newstate

def checkValid(indeces, N):
	validIndeces = []
	for x in indeces:
		if x[0] >= 0 and x[0] < N and x[1] >= 0 and x[1] < N:
			validIndeces.append(x)
	return validIndeces


def isGoal(state):
	N = len(state)
	flatList = []
	testList = []
	if state[N-1][N-1] != "*":
		return False
	tempState = copy.deepcopy(state)
	tempState[N-1].pop(N-1)

	for element in tempState:
		for x in element:
			flatList.append(x)
	testList = sorted(flatList)
	
	if flatList != testList:
		return False
	return True

def BFS(state):
	state1 = copy.deepcopy(state)
	res = tuple(tuple(sublist) for sublist in state1)
	frontier = [state]
	discovered = set()
	parents = {res: None}

	while len(frontier) != 0:
		current_state = frontier.pop(0)
		current_state_T = tuple(tuple(sublist) for sublist in current_state)
		discovered.add(current_state_T)
		
		if isGoal(current_state):
			check = tuple(tuple(sublist) for sublist in current_state)
			path = []
			while check != res:
				puzzle = parents[check] # puzzle now stores the num moved, neighbor
				puzzle_num_moved = puzzle[0] # get the num moved
				path.insert(0, puzzle_num_moved)
				check = tuple(tuple(sublist) for sublist in parents[check][1])
			return path

		for x in ComputeNeighbors(current_state):
			neighbor1 = tuple(tuple(sublist) for sublist in x[1])
			if neighbor1 not in discovered:
				frontier.append(x[1])
				discovered.add(neighbor1)
				parents[neighbor1] = [x[0], current_state]


def DFS(state):
	state1 = copy.deepcopy(state)
	res = tuple(tuple(sublist) for sublist in state1)
	frontier = [state]
	discovered = set()
	parents = {res: None}

	while len(frontier) != 0:
		current_state = frontier.pop(0)
		current_state_T = tuple(tuple(sublist) for sublist in current_state)
		discovered.add(current_state_T)
		
		if isGoal(current_state):
			check = tuple(tuple(sublist) for sublist in current_state)
			path = []
			while check != res:
				puzzle = parents[check] # puzzle now stores the num moved, neighbor
				puzzle_num_moved = puzzle[0] # get the num moved
				path.insert(0, puzzle_num_moved)
				check = tuple(tuple(sublist) for sublist in parents[check][1])
			return path

		for x in ComputeNeighbors(current_state):
			neighbor1 = tuple(tuple(sublist) for sublist in x[1])

			if neighbor1 not in discovered:
				frontier.insert(0,x[1])
				discovered.add(neighbor1)
				parents[neighbor1] = [x[0], current_state]


def buildGoalState(state):
	N = len(state)
	goalState = []

	for x in range(N):
		temp = []
		for i in range(N):
			temp.append(N*x + i)
		goalState.append(temp)


def BidirectionalSearch(state):
	state1 = copy.deepcopy(state)
	res = tuple(tuple(sublist) for sublist in state1)
	frontier = [state]
	discovered = set()
	parents = {res: None}

	goal = buildGoalState(state1)
	frontierB = [goal]
	resB = tuple(tuple(sublist) for sublist in goal)
	discoveredB = set()
	parentsB = {resB: None}

	while len(frontier) != 0 and len(frontierB) != 0:
		current_state = frontier.pop(0)
		current_state_T = tuple(tuple(sublist) for sublist in current_state)
		discovered.add(current_state_T)
		
		current_state_B = frontierB.pop(0)
		current_state_TB = tuple(tuple(sublist) for sublist in current_state_B)
		discoveredB.add(current_state_TB)

		if discoveredB & discovered:
			temp = (discoveredB.intersection(discovered))
			
			#check = tuple(tuple(sublist) for sublist in current_state)
			check = temp.pop()
			checkB = copy.deepcopy(check)
			path = []
			while check != res:
				puzzle = parents[check] # puzzle now stores the num moved, neighbor
				puzzle_num_moved = puzzle[0] # get the num moved
				path.insert(0, puzzle_num_moved)
				check = tuple(tuple(sublist) for sublist in parents[check][1])

			#checkB = tuple(tuple(sublist) for sublist in current_state_B)
			pathB = []
			while checkB != resB:
				puzzleB = parentsB[checkB] # puzzle now stores the num moved, neighbor
				puzzle_num_movedB = puzzleB[0] # get the num moved
				pathB.append(puzzle_num_movedB)
				checkB = tuple(tuple(sublist) for sublist in parentsB[checkB][1])

			return path + pathB

		for x in ComputeNeighbors(current_state):
			neighbor1 = tuple(tuple(sublist) for sublist in x[1])

			if neighbor1 not in discovered:
				frontier.insert(0,x[1])
				discovered.add(neighbor1)
				parents[neighbor1] = [x[0], current_state]

		for i in ComputeNeighbors(current_state_B):
			neighbor1B = tuple(tuple(sublist) for sublist in i[1])

			if neighbor1B not in discoveredB:
				frontierB.insert(0, i[1])
				discoveredB.add(neighbor1B)
				parentsB[neighbor1B] = [i[0], current_state_B]



def DebugPrint(state):
	newState = list(state)
	for x in newState:
		print(str(x), end = "\n")
		

def main():
	state = LoadFromFile("/Users/ishisood/npuzzle/puzzleTest.txt")
	#print(BidirectionalSearch(state))
	print(isGoal(buildGoalState(state)))
	#print(ComputeNeighbors(state))
	#print(BFS(state))
	#nextStates = ComputeNeighbors(state)
	#for x in nextStates:
	#	DebugPrint(x)
	#print(BFS(state))
	#print(BidirectionalSearch(state))
	#print(BFS(state))

    
if __name__ == '__main__':
    main()