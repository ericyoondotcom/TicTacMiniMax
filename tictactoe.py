from os import system
import copy
from random import randrange

class MMNode:
    
    # State: 2D array
    #   -1: Player (X)
    #    0: No one
    #    1: Computer (O)
    #    Computer is always maxie, Player minnie

    def __init__(self, state, maximizer, move):
        self.state = state
        self.maximizer = maximizer
        self.move = move
        self.children = self.generateChildren(move == None)

    def generateChildren(self, log=False):
        children = []
        for row in range(len(self.state)):
            for col in range(len(self.state[row])):
                if self.state[row][col] == 0:
                    newState = copy.deepcopy(self.state)
                    newState[row][col] = -1 if self.maximizer else 1
                    if log:
                        system("clear")
                        printBoard(newState)
                    children.append(MMNode(newState, not self.maximizer, (row, col)))
        
        winner = findWinner(self.state)
        if(winner != 0):
            
            if winner == 42:
                self.value = 0
            elif winner == -1:
                self.value = -50
            elif winner == 1:
                self.value = 50
            return []
        
        if self.maximizer:
            best = -9999
            for child in children:
                '''
                if self.state == [[-1, -1, 1], [0, 1, 0], [-1, -1, 1]]:
                    printBoard(child.state)
                    print("Child value: ", child.value, "Best so far: ", best)
                    input("Press to continue")
                '''
                if child.value > best or (child.value == best and randrange(2) == 0):
                    self.favoriteChild = child
                    best = child.value
        else:
            best = 9999
            for child in children:
                if child.value < best or (child.value == best and randrange(2) == 0):
                    self.favoriteChild = child
                    best = child.value
        self.value = best
        return children

# I literally only have this bc I don't want to rewrite each condition :/
def findWinner(state, log=False):
    if findWinnerHelper(state, -1, log):
        return -1
    if findWinnerHelper(state, 1, log):
        return 1

    for row in state:
        for i in row:
            if i == 0:
                return 0
    return 42 #42 is Tie case

def findWinnerHelper(state, player, log=False):
    if state[0][0] == player and state[1][1] == player and state[2][2] == player:
        if log:
            print("Found down-rightwards diagonal match")
        return True
    if state[2][0] == player and state[1][1] == player and state[0][2] == player:
        if log:
            print("Found down-leftwards diagonal match")
        return True
    for i in range(len(state)):
        found = True
        for j in range(len(state[i])):
            if state[i][j] != player:
                found = False
                break
        if found:
            if log:
                print("Found match in row ", i)
            return True
    for i in range(len(state)):
        found = True
        for j in range(len(state[i])):
            if state[j][i] != player:
                found = False
                break
        if found:
            if log:
                print("Found match in col ", i)
            return True
    

def userMove(gameState):
    inp = input("Your turn!\nUse QWE/ASD/ZXC for input. >")
    if inp == "q" or inp == "a" or inp == "z":
        col = 0
    elif inp == "w" or inp == "s" or inp == "x":
        col = 1
    elif inp == "e" or inp == "d" or inp == "c":
        col = 2
    if inp == "q" or inp == "w" or inp == "e":
        row = 0
    elif inp == "a" or inp == "s" or inp == "d":
        row = 1
    elif inp == "z" or inp == "x" or inp == "c":
        row = 2
    if gameState.state[row][col] != 0:
        while True:
            print(gameState.state[row][col])
            print("Cheaters never win")

    found = False
    for child in gameState.children:
        if child.move == (row, col):
            found = True
            return child
            break

    if not found:
        raise Exception("Children did not contain the move.")

def computerMove(gameState):
    return gameState.favoriteChild

def printBoard(state):
    for row in state:
        print("|", end="")
        for i in row:
            if i == -1:
                char = "X"
            elif i == 1:
                char = "O"
            else:
                char = " "
            print(char, end=" ")
        print("|")
    print("")

print("Welcome to Tic Tac Toe, where you never win!®")
print("Do you want to go first?")

root = MMNode([[0, 0, 0], [0, 0, 0], [0, 0, 0]], not ("n" in input("(Y/n) > ")), None)
gameState = root

while True:
    while True:
        #system('clear')
        printBoard(gameState.state)
        print("Score: ", gameState.value)

        if gameState.maximizer:
                print("I AM MAXIMIZER")
        for c in gameState.children:
            printBoard(c.state)
            print(c.value)
        print("best: ", gameState.favoriteChild.value)
        #if gameState.maximizer:
        if input("Type r for computery help!") != "r":
            suggested = gameState.favoriteChild.move
            print("Suggested move: (", suggested[0] + 1, ", ", suggested[1] + 1, ")", sep="")
            gameState = userMove(gameState)
        else:
            print("Computer is thinking...")
            gameState = computerMove(gameState)

        winner = findWinner(gameState.state)

        if winner != 0:
            printBoard(gameState.state)
            print(findWinner(gameState.state))
            print(gameState.value)
            if winner == 42:
                print("Tie! Nobody wins. (Don't feel bad, this is the best outcome you can get)")
            elif winner == -1:
                print("Minimax was supposed to ensure you can't win, but you did. Tell Eric it's time to debug :(")
            elif winner == 1:
                print("You lose! lol")
            else:
                raise Exception("Unexpected return from findWinner(): " + str(winner))
            break
    
    print("Game over! Do you want to play again? (If you want to change your going-first preference, say no)")
    if "n" in input("(Y/n) > "):
        exit()
    gameState = root