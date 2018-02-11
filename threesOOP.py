#threesOOP.py - A threes game object, in Python3
#Deric Miller - 2017

import numpy
import math
import random

class threesOOP():
    def __init__(self):
        self.isover = 0
        self.deck = self.getBaseDeck()
        self.board = numpy.zeros(shape=(4,4), dtype = int)
        self.spots = numpy.random.permutation(numpy.arange(15)) #Randomly pick the places for the first 9 cards...
        for i in range(9): #...and place them.
            self.card, self.deck = self.deck[-1], self.deck[:-1]
            self.smeg, self.spots = self.spots[-1], self.spots[:-1]
            self.board[self.smeg % 4, math.floor(self.smeg/4)] = self.card
        self.maxcard = numpy.amax(self.board)
        self.cardchoice, self.deck = self.chooseCard(self.deck, self.maxcard)
    
    def getStatus(self):
        self.counts = [numpy.count_nonzero(self.deck == 1), numpy.count_nonzero(self.deck == 2), numpy.count_nonzero(self.deck == 3)] #get the counts of the deck
        self.cardvis = self.cardchoice if self.cardchoice <= 3 else 4
        self.currscore = self.countScore(self.board)
        self.isover = self.checkForDone(self.board)
        return[self.board, self.counts, self.cardvis, self.currscore, self.isover]
    
    def getBaseDeck(self):
        baseDeck = numpy.random.permutation(numpy.array([1,1,1,1,2,2,2,2,3,3,3,3]))
        return baseDeck
      
    def checkForDone(self, board):
        #boardtmp = board
        self.possiblepositions = []
        for self.i in range(3):            
            for self.j in range(4):
                if self.board[self.i,self.j] == 0 and self.board[self.i+1,self.j] > 0:
                    self.possiblepositions.append(self.j)
                elif self.board[self.i,self.j] == 1 and self.board[self.i+1,self.j] == 2:
                    self.possiblepositions.append(self.j)
                elif self.board[self.i,self.j] == 2 and self.board[self.i+1,self.j] == 1:
                    self.possiblepositions.append(self.j)
                elif self.board[self.i,self.j] > 2 and self.board[self.i,self.j] == self.board[self.i+1,self.j]:
                    self.possiblepositions.append(self.j)
        for self.i in range(3,0,-1):            
            for self.j in range(4):
                if self.board[self.i,self.j] == 0 and self.board[self.i-1,self.j] > 0:
                    self.possiblepositions.append(self.j)
                elif self.board[self.i,self.j] == 1 and self.board[self.i-1,self.j] == 2:
                    self.possiblepositions.append(self.j)
                elif self.board[self.i,self.j] == 2 and self.board[self.i-1,self.j] == 1:
                    self.possiblepositions.append(self.j)
                elif self.board[self.i,self.j] > 2 and self.board[self.i,self.j] == self.board[self.i-1,self.j]:
                    self.possiblepositions.append(self.j)
        for self.j in range(3):
            for self.i in range(4):
                if self.board[self.i,self.j] == 0 and self.board[self.i,self.j+1] > 0:
                    self.possiblepositions.append(self.i)
                elif self.board[self.i,self.j] == 1 and self.board[self.i,self.j+1] == 2:
                    self.possiblepositions.append(self.i)
                elif self.board[self.i,self.j] == 2 and self.board[self.i,self.j+1] == 1:
                    self.possiblepositions.append(self.i)
                elif self.board[self.i,self.j] > 2 and self.board[self.i,self.j] == self.board[self.i,self.j+1]:
                    self.possiblepositions.append(self.i)
        for self.j in range(3,0,-1):
            for self.i in range(4):
                if self.board[self.i,self.j] == 0 and self.board[self.i,self.j-1] > 0:
                    self.possiblepositions.append(self.i)
                elif self.board[self.i,self.j] == 1 and self.board[self.i,self.j-1] == 2:
                    self.possiblepositions.append(self.i)
                elif self.board[self.i,self.j] == 2 and self.board[self.i,self.j-1] == 1:
                    self.possiblepositions.append(self.i)
                elif self.board[self.i,self.j] > 2 and self.board[self.i,self.j] == self.board[self.i,self.j-1]:
                    self.possiblepositions.append(self.i)
        if len(self.possiblepositions) > 0: #Did a Move Happen?
            return 0
        else:
            return 1
    
    def getPlusCard(maxcard):
        self.pluscards = (numpy.log2((self.maxcard)/3))-3
        self.smeg = random.randint(1,self.pluscards)
        self.randplus = int(((2**(self.smeg+3))*3)/8)
        return self.randplus
    
    def chooseCard(self, deck, maxcard):
        if random.randint(0,20) == 0 and self.maxcard >= 48:
            self.cardchoice = getPlusCard(self.maxcard)
            print(self.cardchoice)
        else:
            numpy.random.permutation(self.deck)
            self.cardchoice, self.deck = self.deck[-1], self.deck[:-1]
        return self.cardchoice, self.deck
            
    def makeMove(self, move):
        self.possiblepositions = []
        if move == 'u':        
            for self.i in range(3):            
                for self.j in range(4):
                    if self.board[self.i,self.j] == 0 and self.board[self.i+1,self.j] > 0:
                        self.board[self.i,self.j] = self.board[self.i+1, self.j]
                        self.board[self.i+1,self.j] = 0
                        self.possiblepositions.append(self.j)
                    elif self.board[self.i,self.j] == 1 and self.board[self.i+1,self.j] == 2:
                        self.board[self.i,self.j] = 3
                        self.board[self.i+1,self.j] = 0
                        self.possiblepositions.append(self.j)
                    elif self.board[self.i,self.j] == 2 and self.board[self.i+1,self.j] == 1:
                        self.board[self.i,self.j] = 3
                        self.board[self.i+1,self.j] = 0
                        self.possiblepositions.append(self.j)
                    elif self.board[self.i,self.j] > 2 and self.board[self.i,self.j] == self.board[self.i+1,self.j]:
                        self.board[self.i,self.j] = self.board[self.i,self.j] * 2
                        self.board[self.i+1,self.j] = 0
                        self.possiblepositions.append(self.j)
            if len(self.possiblepositions) > 0: #Did a Move Happen?            
                self.board[3,random.choice(self.possiblepositions)] = self.cardchoice
                self.cardchoice, self.deck = self.chooseCard(self.deck, numpy.amax(self.board))
                
        elif move == 'd':
            for self.i in range(3,0,-1):            
                for self.j in range(4):
                    if self.board[self.i,self.j] == 0 and self.board[self.i-1,self.j] > 0:
                        self.board[self.i,self.j] = self.board[self.i-1, self.j]
                        self.board[self.i-1,self.j] = 0
                        self.possiblepositions.append(self.j)
                    elif self.board[self.i,self.j] == 1 and self.board[self.i-1,self.j] == 2:
                        self.board[self.i,self.j] = 3
                        self.board[self.i-1,self.j] = 0
                        self.possiblepositions.append(self.j)
                    elif self.board[self.i,self.j] == 2 and self.board[self.i-1,self.j] == 1:
                        self.board[self.i,self.j] = 3
                        self.board[self.i-1,self.j] = 0
                        self.possiblepositions.append(self.j)
                    elif self.board[self.i,self.j] > 2 and self.board[self.i,self.j] == self.board[self.i-1,self.j]:
                        self.board[self.i,self.j] = self.board[self.i,self.j] * 2
                        self.board[self.i-1,self.j] = 0
                        self.possiblepositions.append(self.j)
            if len(self.possiblepositions) > 0: #Did a Move Happen?            
                self.board[0,random.choice(self.possiblepositions)] = self.cardchoice
                self.cardchoice, self.deck = self.chooseCard(self.deck, numpy.amax(self.board))
                            
        elif move == 'l':
            for self.j in range(3):
                for self.i in range(4):
                    if self.board[self.i,self.j] == 0 and self.board[self.i,self.j+1] > 0:
                        self.board[self.i,self.j] = self.board[self.i, self.j+1]
                        self.board[self.i,self.j+1] = 0
                        self.possiblepositions.append(self.i)
                    elif self.board[self.i,self.j] == 1 and self.board[self.i,self.j+1] == 2:
                        self.board[self.i,self.j] = 3
                        self.board[self.i,self.j+1] = 0
                        self.possiblepositions.append(self.i)
                    elif self.board[self.i,self.j] == 2 and self.board[self.i,self.j+1] == 1:
                        self.board[self.i,self.j] = 3
                        self.board[self.i,self.j+1] = 0
                        self.possiblepositions.append(self.i)
                    elif self.board[self.i,self.j] > 2 and self.board[self.i,self.j] == self.board[self.i,self.j+1]:
                        self.board[self.i,self.j] = self.board[self.i,self.j] * 2
                        self.board[self.i,self.j+1] = 0
                        self.possiblepositions.append(self.i)
            if len(self.possiblepositions) > 0: #Did a Move Happen?            
                self.board[random.choice(self.possiblepositions), 3] = self.cardchoice
                self.cardchoice, self.deck = self.chooseCard(self.deck, numpy.amax(self.board))
                        
        elif move == 'r':
            for self.j in range(3,0,-1):
                for self.i in range(4):
                    if self.board[self.i,self.j] == 0 and self.board[self.i,self.j-1] > 0:
                        self.board[self.i,self.j] = self.board[self.i, self.j-1]
                        self.board[self.i,self.j-1] = 0
                        self.possiblepositions.append(self.i)
                    elif self.board[self.i,self.j] == 1 and self.board[self.i,self.j-1] == 2:
                        self.board[self.i,self.j] = 3
                        self.board[self.i,self.j-1] = 0
                        self.possiblepositions.append(self.i)
                    elif self.board[self.i,self.j] == 2 and self.board[self.i,self.j-1] == 1:
                        self.board[self.i,self.j] = 3
                        self.board[self.i,self.j-1] = 0
                        self.possiblepositions.append(self.i)
                    elif self.board[self.i,self.j] > 2 and self.board[self.i,self.j] == self.board[self.i,self.j-1]:
                        self.board[self.i,self.j] = self.board[self.i,self.j] * 2
                        self.board[self.i,self.j-1] = 0
                        self.possiblepositions.append(self.i)
            if len(self.possiblepositions) > 0: #Did a Move Happen?            
                self.board[random.choice(self.possiblepositions), 0] = self.cardchoice
                self.cardchoice, self.deck = self.chooseCard(self.deck, numpy.amax(self.board))
                
            
        if len(self.deck) == 0:
            self.deck = self.getBaseDeck()
        return self.board, self.deck, self.cardchoice
    
    def countScore(self, board):
        self.scoreboard = numpy.copy(self.board)    
        self.scoreboard = numpy.power(3,(numpy.log2(numpy.divide(self.scoreboard+.00001, 3))+1))
        #print(scoreboard.astype(int))
        self.scoreboard[self.scoreboard < 3] = 0
        return numpy.sum(self.scoreboard, dtype = int)
            
    def main():
        self.movecounter = 0
        arrowchar = {'\x1b[A':'u', '\x1b[B':'d','\x1b[C':'r','\x1b[D':'l','qqq':'q'}
        self.cardchoice, self.deck = chooseCard(self.deck, numpy.amax(self.board))
        drawItAll(self.board, self.deck, self.movecounter, self.cardchoice)
        while checkForDone(self.board) == 0:       
            try:
                self.smeg = getChar()
                self.inkey = arrowchar[self.smeg]
                self.movecounter += 1
                print(self.inkey)
                self.board, self.deck, self.cardchoice = makeMove(self.board, self.inkey, self.deck, self.cardchoice)
                drawItAll(self.board, self.deck, self.movecounter, self.cardchoice)
            except KeyError:
                print("notArrow")
        print(self.board)
        #print("postloop")
        #print(movecounter)
        self.finalscore = countScore(self.board)
        print(self.finalscore)