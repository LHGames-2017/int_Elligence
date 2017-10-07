# Author: Kyle Kastner
# License: BSD 3-Clause
# Implementing http://mnemstudio.org/path-finding-q-learning-tutorial.htm
# Q-learning formula from http://sarvagyavaish.github.io/FlappyBirdRL/
# Visualization based on code from Gael Varoquaux gael.varoquaux@normalesup.org
# http://scikit-learn.org/stable/auto_examples/applications/plot_stock_market.html

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# defines the reward/connection graph
def print_deserialized_map(map):
    for i in range(20):
        tmp = []
        for j in range(20):
            tmp.append(map[i][j].Content)
        print(tmp)

def build_r(deserialized_map):
    r = []
    switcher = {
        0: 0,
        1: 100,
        2: 50,
        3: 200,
        4: -100,
        5: -1000,
        6: 50,
    }
    for i in range(20):
        col = []
        for j in range(20):
            col.append(switcher[deserialized_map[i][j].Content])
        print(col)
        r.append(col)
    return np.array(r)

def update_q(state, next_state, action, alpha, gamma, r, q):
    rsa = r[state, action]
    qsa = q[state, action]
    new_q = qsa + alpha * (rsa + gamma * max(q[next_state, :]) - qsa)
    q[state, action] = new_q
    # renormalize row to be between 0 and 1
    rn = q[state][q[state] > 0] / np.sum(q[state][q[state] > 0])
    q[state][q[state] > 0] = rn
    return r[state, action]

# Core algorithm
def apply_QL(r, q):
    gamma = 0.8
    alpha = 1.
    n_episodes = 1E3
    n_states = 6
    n_actions = 6
    epsilon = 0.05
    random_state = np.random.RandomState(1999)
    for e in range(int(n_episodes)):
        states = list(range(n_states))
        random_state.shuffle(states)
        current_state = states[0]
        goal = False
        if e % int(n_episodes / 10.) == 0 and e > 0:
            pass
            # uncomment this to see plots each monitoring
            #show_traverse()
            #show_q()
        while not goal:
            # epsilon greedy
            valid_moves = r[current_state] >= 0
            if random_state.rand() < epsilon:
                actions = np.array(list(range(n_actions)))
                actions = actions[valid_moves == True]
                if type(actions) is int:
                    actions = [actions]
                random_state.shuffle(actions)
                action = actions[0]
                next_state = action
            else:
                if np.sum(q[current_state]) > 0:
                    action = np.argmax(q[current_state])
                else:
                    # Don't allow invalid moves at the start
                    # Just take a random move
                    actions = np.array(list(range(n_actions)))
                    actions = actions[valid_moves == True]
                    random_state.shuffle(actions)
                    action = actions[0]
                next_state = action
            reward = update_q(current_state, next_state, action,
                            alpha=alpha, gamma=gamma, r=r, q=q)
            # Goal state has reward 100
            if reward > 1:
                goal = True
            current_state = next_state
    return q
