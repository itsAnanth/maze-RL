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
    
    def getIndex(self):
        copy = self.state.copy().tolist()
        frac, whole = math.modf(self.currentState / 4)
        row = math.floor(whole)
        col = [0, 0.25, 0.5, 0.75].index(frac)
        return row, col

    
    def displayState(self):
        
        copy = self.state.copy().tolist()
        row, col = self.getIndex()
        copy[row][col] = 'x'
        print(tabulate(copy, tablefmt='grid'))

    def getAction(self):
        validActions = list(self.actionsMap.values())
        row, col = self.getIndex()

        if row == 0:
            validActions[self.actionsMap['up']] = -1
        if row == self.state.shape[0] - 1:
            validActions[self.actionsMap['down']] = -1

        if col == 0:
            validActions[self.actionsMap['left']] = -1
        if col == self.state.shape[1] - 1:
            validActions[self.actionsMap['right']] = -1

        return validActions

        
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
