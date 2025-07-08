import numpy as np
from tabulate import tabulate
import math

class Environment:

    def __init__(self):
        self.statesMap = {
            'valid': 0,
            'dead': -1,
            'goal': 1
        }
        self.actionsMap = { action: i for i, action in enumerate(['up', 'down', 'left', 'right'])}
        self.state = None
        self.actions = None
        self.currentState = None

        self.initialize()
        

    def initialize(self):
        self.state = np.zeros(shape=(4, 4), dtype=int)
        self.currentState = 0

        self.state[1][1] = self.statesMap['dead']
        self.state[3][3] = self.statesMap['goal']

    def generateAction(self, *actions):
        final = np.array([-1] * 4, dtype=int)
        for action in actions:
            final[self.actionsMap[action]] = 1
        return final
    
    def displayState(self):
        copy = self.state.copy().tolist()
        frac, whole = math.modf(self.currentState / 4)
        row = math.floor(whole)
        col = [0, 0.25, 0.5, 0.75].index(frac)
        print(row, col)
        copy[row][col] = 'x'

        print(tabulate(copy, tablefmt='grid'))

    def getAction(self):
        if self.currentState == 0:
            return self.generateAction('right', 'down')
        elif self.currentState == 3:
            return self.generateAction('left', 'down')
        elif self.currentState == 12:
            return self.generateAction('up', 'right')
        elif self.currentState == 15:
            return self.generateAction('up', 'left')
        elif self.currentState in [1, 2]:
            return self.generateAction('left', 'right', 'down')
        elif self.currentState in [4, 8]:
            return self.generateAction('up', 'down', 'right')
        elif self.currentState in [7, 11]:
            return self.generateAction('up', 'down', 'left')
        elif self.currentState in [13, 14]:
            return self.generateAction('left', 'right', 'up')
        else:
            return self.generateAction('up', 'down', 'left', 'right')
        
    def performAction(self):
        validActions = [i for i, v in enumerate(self.getAction()) if v != -1]
        choice = np.random.choice(validActions)
        movements = [['up', -4], ['down', 4], ['left', -1], ['right', 1]]
        
        for movement in movements:
            name, magnitude = movement
            if self.actionsMap[name] == choice:
                print(name, magnitude)

                self.currentState += magnitude
                return


env = Environment()
env.displayState()
env.performAction()
env.displayState()
