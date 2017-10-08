# Author: Kyle Kastner
# License: BSD 3-Clause
# Implementing http://mnemstudio.org/path-finding-q-learning-tutorial.htm
# Q-learning formula from http://sarvagyavaish.github.io/FlappyBirdRL/
# Visualization based on code from Gael Varoquaux gael.varoquaux@normalesup.org
# http://scikit-learn.org/stable/auto_examples/applications/plot_stock_market.html

import numpy as np
from random import randint

# defines the reward/connection graph
def print_deserialized_map(map):
    for i in range(20):
        tmp = []
        for j in range(20):
            tmp.append(map[i][j].Content)
        print(tmp)

# Construit la matrice de récompense r.
# 1ere dim: position x d'une case de la carte
# 2e dim: position y d'une case de la carte
# 3e dim: différentes actions possibles (miner,bouger)
# Contenu de chaque case: récompense r selon une action et un point de la carte.
def build_r(deserialized_map):

    r = [[[0 for k in range(8)]  for j in range(20)] for i in range(20)]
    # Indice de 3e dimension de la matrice r. Représente chaque action implémentés (il y en a plus, mais faute de temps...)
    # 0 Move left
    # 1 Move Right
    # 2 Move up
    # 3 Move Down
    # 4 Collect left
    # 5 Collect Right
    # 6 Collect up
    # 7 Collect down

    for i in range(20):
        for j in range(20):
            #Si case gauche empty ou house ou lava
            switcherMove = {
                    0:    5,
                    1: -100,
                    2:    7,
                    3: -100,
                    4: -100,
                    5: -100,
                    6: -100
            }
            switcherCollect = {
                    0: -100,
                    1: -100,
                    2: -100,
                    3: -100,
                    4:   40,
                    5: -100,
                    6: -100
            }

            if(j > 0):
                r[i][j][0] = switcherMove[deserialized_map[i][j-1].Content] #Attribue à la case gauche du joueur un reward pour marcher
                r[i][j][4] = switcherCollect[deserialized_map[i][j-1].Content] #Attribue à la case gauche du joueur un reward pour collecter
            if(j < 19):
                r[i][j][1] = switcherMove[deserialized_map[i][j+1].Content] #Attribue à la case droite du joueur un reward pour marcher
                r[i][j][5] = switcherCollect[deserialized_map[i][j+1].Content] #Attribue à la case gauche du joueur un reward pour collecter
            if(i > 0):
                r[i][j][2] = switcherMove[deserialized_map[i-1][j].Content] #Attribue à la case up du joueur un reward pour marcher
                r[i][j][6] = switcherCollect[deserialized_map[i-1][j].Content] #Attribue à la case up du joueur un reward pour collecter
            if(i < 19):
                r[i][j][3] = switcherMove[deserialized_map[i+1][j].Content] #Attribue à la case down du joueur un reward pour marcher
                r[i][j][7] = switcherCollect[deserialized_map[i+1][j].Content] #Attribue à la case down du joueur un reward pour collecter

    return r

#Permet de choisir l'action selon la matrice r.
def choisir_action(x, y,r):
    rNb = (randint(0,10))
    action = 0
    if(rNb < 9): #8/10 de choisir la meilleure action
        for i in range(8):
            if(r[x][y][i] > r[x][y][action]):
                action = i
    else: #2/10 de choisir n'importequelle action POSSIBLE pour trouver de nouvelles possibilité
        estPossible = False
        while(estPossible == False):
            action = (randint(0,7))
            if (r[x][y][action] >= 0):
                estPossible = True
    return action

def findMaxQ(nextPosX, nextPosY, q):
    maxQ = 0
    for i in range(8):
        if (q[nextPosX][nextPosY][i] > maxQ):
            maxQ = q[nextPosX][nextPosY][i]
    return maxQ

