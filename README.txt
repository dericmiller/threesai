ThreesAI is an implementation of the game Threes ( http://play.threesgame.com/ ) in Python 3 for training neural nets to play, and includes a pretrained net that performs better than random at Threes.  There remains room for a significant improvement in the AI.

ThreesAI requires Python 3, as well as keras, numpy, sys, tty, termios, and csv.

The threesAI.py file contains the overall management code that handles both the game object (threesOOP) and either the AI object (AIOOP) or the input from a human player.

To play a game of Threes on the command line using human inputs, run:

python3 ./threesAI.py

Use the arrow keys to make moves, and hit 'q' three times to quit the game early.


To have the current AI model play 1000 games and report basic summary stats of its results, run:

python3 ./threesAI.py ai

The game records the scores of all of its games in the most recent run in the file gamesHistory.csv if you're interested in running more robust statistical analyisis of its performance.


To train a new AI model, run:

python3 ./threesAI.py ai new


To add training games to the existing model, run:

python3 ./threesAI.py ai train


Lines 20 - 24 of AIOOP.py contain different ways to automate move generation.  Only one of these lines should be uncommented; by changing which one, you can explore the performance of several nieve strategies at Threes and compare them to your Neural Net.  Getting the Neural Net to perform better than random has proven extremely straightforward.  