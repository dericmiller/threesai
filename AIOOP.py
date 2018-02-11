import random
import numpy

#The AI player object.  To pick a naive stratgy instead of using the Neural Net, change which of the getMove lines is uncommented in the getMove method. 

class AIOOP():
    def __init__(self, model):
        self.possmoves = numpy.array(['u','d','l','r'])
        self.model = model
    
    def getMove(self, gamestatus):
        self.gamestatus = gamestatus
        #return[self.board, self.counts, self.cardvis, self.currscore, self.isover]
        self.board = self.gamestatus[0]
        #self.counts = self.gamestatus[1]
        #self.cardvis = self.gamestatus[2]
        #self.currscore = self.gamestatus[3]
        #self.isover = self.gamestatus[4]
        
        #move = self.getMoveRando()
        #move = self.getMoveCorner1(self.board)
        #move = self.getMoveCorner2(self.board)        
        #move = self.getMoveCorner3(self.board)                   
        move = self.getMoveNN(self.gamestatus)
        #print(move)
        return move
    
    def getMoveRando(self):
        #dummy AI: move at random:
        move = numpy.random.choice(self.possmoves)
        #print(move)
        return move
    
    def getMoveCorner1(self, board):
        #Right, Down, Left, Up
        if(self.checkDirection(self.board, 3)):
            #print(self.possmoves[3])
            return self.possmoves[3]
        elif(self.checkDirection(self.board, 1)):
            return self.possmoves[1]
        elif(self.checkDirection(self.board, 2)):
            return self.possmoves[2]
        else:
            return self.possmoves[0]
        
    def getMoveCorner2(self, board):
        #Right, Down, Up, Left
        if(self.checkDirection(self.board, 3)):
            return 'r'
        elif(self.checkDirection(self.board, 1)):
            return 'd'
        elif(self.checkDirection(self.board, 0)):
            return 'u'
        else:
            return 'l'
        
    def getMoveCorner3(self, board):
        #Right, Left, Down, Up
        if(self.checkDirection(self.board, 3)):
            return 'r'
        elif(self.checkDirection(self.board, 2)):
            return 'l'
        elif(self.checkDirection(self.board, 1)):
            return 'd'
        else:
            return 'u'
    
    def getMoveNN(self, gamestatus):
        #Input Layer - 20 neurons: 16 board squares, 3 deck counts, 1 next card
        #Output Layer - 4 neruon softmax: up, down, left, and right
        #gamesatus: [self.board, self.counts, self.cardvis, self.currscore, self.isover]
        self.modelIn = numpy.concatenate((self.gamestatus[0].reshape(16, 1), numpy.array(self.gamestatus[1]).reshape(3,1), numpy.array([[self.gamestatus[2]]])))
        #self.modelIn = numpy.concatenate(self.gamestatus[0].reshape(1, 16), self.gamestatus[1].reshape(1,3), self.gamestatus[2])
        self.qval = self.model.predict(self.modelIn.reshape(1,20), batch_size=1)
        self.order = numpy.argsort(self.qval)
        for i in range(0, 4):
            #print(i)
            #print(self.order)
            #print(self.order[i])
            #print(self.order[0, 1])
            #print(self.order[1, 0])
            if(self.checkDirection(self.board,self.order[0, i])):
                move = self.possmoves[(self.order[0,i])] #take action with highest Q-value
                break         
        return move

    def checkDirection(self, board, direction):
        #Up
        if direction == 0:
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
            if len(self.possiblepositions) > 0: #Did a Move Happen?
                return 1
            else:
                return 0
        #Down
        elif direction == 1:
            self.possiblepositions = []
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
            if len(self.possiblepositions) > 0: #Did a Move Happen?
                return 1
            else:
                return 0
        #Left
        elif direction == 2:
            self.possiblepositions = []
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
            if len(self.possiblepositions) > 0: #Did a Move Happen?
                return 1
            else:
                return 0
        #Right
        elif direction == 3:
            self.possiblepositions = []        
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
                return 1
            else:
                return 0
        else:
            return "ERROR CODE SIGMA"