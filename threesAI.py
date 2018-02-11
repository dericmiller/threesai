import threesOOP
import AIOOP
import numpy
import sys
import tty
import termios
import csv

import os
from keras.models import Sequential
from keras.models import load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
import random

possmoves = numpy.array(['u','d','l','r'])

#This file contains the overall management code.  It deals with both the game object (from threesOOP) and either the artificial intelligence object (from AIOOP) or a human player.

def mainAI():
    theplayer = AIOOP.AIOOP(model)
    thegame = threesOOP.threesOOP()
    while not thegame.isover:
        gamestatus = thegame.getStatus()
        move = theplayer.getMove(gamestatus)
        thegame.makeMove(move)
        gamestatus = thegame.getStatus()
        isover = gamestatus[4]
        #print(gamestatus[0])
    return gamestatus[3]

def mainHuman():
    arrowchar = {'\x1b[A':'u', '\x1b[B':'d','\x1b[C':'r','\x1b[D':'l','qqq':'q'}
    thegame = threesOOP.threesOOP()
    gamestatus = thegame.getStatus()
    print(gamestatus[0])
    print('Next: ' + str(gamestatus[2]))      
    while not thegame.isover:
        move = arrowchar[getChar()]
        if move == 'q':
            sys.exit()
        print(move)
        thegame.makeMove(move)
        gamestatus = thegame.getStatus()
        isover = gamestatus[4]
        print(gamestatus[0])
        print('Next: ' + str(gamestatus[2]))     
    return gamestatus[3]

def getChar():
    #MODIFIED FROM HERE (EXAMPLE 5):
    #http://www.programcreek.com/python/example/51345/termios.TCSADRAIN
    #Grabs a character from stdin.
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3) #The arrow keys are 3 character combos, so to grab them you have to grab 3 characters.  Which breaks all the other keys.  Which is why you have to hit qqq to quit.
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def buildModel():
    model = Sequential()
    model.add(Dense(120, init='lecun_uniform', input_shape=(20,)))
    model.add(Activation('relu'))
    #model.add(Dropout(0.2)) I'm not currently using dropout, but it may be worth investigating.    
    model.add(Dense(100, init='lecun_uniform'))
    model.add(Activation('relu'))
    #model.add(Dropout(0.2))    
    model.add(Dense(4, init='lecun_uniform'))
    model.add(Activation('linear')) #linear output so we can have range of real-valued outputs 
    model.compile(loss='mse', optimizer=RMSprop())
    return model

def train(model):
    epochs = 10
    gamma = 0.175
    epsilon = 1
    batchSize = 40
    buffer = 80
    reward = 0
    replay = []
    #stores tuples of (S, A, R, S')
    h = 0
    for i in range(epochs):
        thegame = threesOOP.threesOOP()
        dispFlag = 0
        if i % 20 == 0:
            print("Game #: %s" % (i,))
            print("Reward: %s" % (reward,))
            dispFlag = 1
            if i % 2000 == 0:
                model.save('my_model-%d.h5' % (i,))
        #os.system('clear')
        while not thegame.isover:
            gamestatus = thegame.getStatus()
            #print(gamestatus[0].reshape(16, 1))
            #print(numpy.array(gamestatus[1]).reshape(1,3))
            #print(numpy.array([[gamestatus[2]]]))
            modelIn = numpy.concatenate((gamestatus[0].reshape(16, 1), numpy.array(gamestatus[1]).reshape(3,1), numpy.array([[gamestatus[2]]])))
            qval = model.predict(modelIn.reshape(1,20), batch_size=1)
            if (random.random() < epsilon): #choose random action
                action = numpy.random.randint(0,4)
            else: #choose best action from Q(s,a) values
                action = (numpy.argmax(qval))
            #Take action, observe new state S'
            new_state = thegame.makeMove(possmoves[action])
            #Observe reward
            gamestatus2 = thegame.getStatus()
            new_state = numpy.concatenate((gamestatus2[0].reshape(16, 1), numpy.array(gamestatus2[1]).reshape(3,1), numpy.array([[gamestatus2[2]]])))
            reward = gamestatus2[3]
            #Experience replay storage
            if (len(replay) < buffer): #if buffer not filled, add to it
                replay.append((modelIn, action, reward, new_state))
            else: #if buffer full, overwrite old values
                if (h < (buffer-1)):
                    h += 1
                else:
                    h = 0
                replay[h] = (modelIn, action, reward, new_state)
                #randomly sample our experience replay memory
                minibatch = random.sample(replay, batchSize)
                X_train = []
                y_train = []
                for memory in minibatch:
                    #Get max_Q(S',a)
                    old_state, action, reward, new_state = memory
                    old_qval = model.predict(old_state.reshape(1,20), batch_size=1)
                    newQ = model.predict(new_state.reshape(1,20), batch_size=1)
                    maxQ = numpy.max(newQ)
                    y = numpy.zeros((1,4))
                    y[:] = old_qval[:]
                    if reward == -1: #non-terminal state
                        update = (reward + (gamma * maxQ))
                    else: #terminal state
                        update = reward
                    y[0][action] = update
                    X_train.append(old_state.reshape(20,))
                    y_train.append(y.reshape(4,))    
                X_train = numpy.array(X_train)
                y_train = numpy.array(y_train)
                model.fit(X_train, y_train, batch_size=batchSize, nb_epoch=1, verbose=0)
                state = new_state
            if reward != -1: #if reached terminal state, update game status
                status = 0
        if epsilon > 0.1: #decrement epsilon over time
            epsilon -= (1/epochs)
    #save_model(model)
    model.save('my_model.h5')

if __name__ == "__main__":
    if((len(sys.argv)>1) and (str(sys.argv[1]) == 'ai' or str(sys.argv[1]) == 'AI')):
        if((len(sys.argv)>2) and (str(sys.argv[2]) == 'train')):
            model=load_model('my_model.h5')
            train(model)
        elif((len(sys.argv)>2) and (str(sys.argv[2]) == 'new')):
            model = buildModel()
            train(model)
        else:
            model=load_model('my_model.h5')
        scorearray = numpy.zeros(shape=(1000), dtype=int)
        for zed in range(1000):
            scorearray[zed] = mainAI()
        print('Siz: ' + str(scorearray.size))
        print('Max: ' + str(numpy.amax(scorearray)))
        print('Min: ' + str(numpy.amin(scorearray)))
        print('Avg: ' + str(numpy.mean(scorearray)))
        print('Med: ' + str(numpy.median(scorearray)))
        csvfile = "./gamesHistory.csv"
        with open(csvfile, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            for val in scorearray:
                #print(val)
                writer.writerow([val])
    else:
        score = mainHuman()
        print('Final Score: ' + str(score))