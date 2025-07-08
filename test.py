import numpy as np
from tabulate import tabulate

class Environment:

    def __init__(self):
        self.statesMap = {
            'valid': 0,
            'dead': -1,
            'goal': 1
        }
        self.actionsMap = { action: i for i, action in enumerate(['up', 'down', 'left', 'right']) }
        self.reverseActionsMap = { v: k for k, v in self.actionsMap.items() }
        self.state = None
        self.currentState = None
        self.qtable = {}

        self.initialize()

    def initialize(self):
        self.state = np.zeros((4, 4), dtype=int)
        self.state[1][1] = self.statesMap['dead']
        self.state[3][3] = self.statesMap['goal']
        self.currentState = (0, 0)

    def reset(self):
        self.currentState = (0, 0)
        return self.currentState

    def displayState(self):
        copy = self.state.copy().tolist()
        row, col = self.currentState
        copy[row][col] = 'x'
        print(tabulate(copy, tablefmt='grid'))

    def getValidActions(self, state=None):
        if state is None:
            row, col = self.currentState
        else:
            row, col = state

        actions = []
        if row > 0:
            actions.append(self.actionsMap['up'])
        if row < 3:
            actions.append(self.actionsMap['down'])
        if col > 0:
            actions.append(self.actionsMap['left'])
        if col < 3:
            actions.append(self.actionsMap['right'])
        return actions

    def move(self, action):
        row, col = self.currentState
        if action == self.actionsMap['up']:
            row -= 1
        elif action == self.actionsMap['down']:
            row += 1
        elif action == self.actionsMap['left']:
            col -= 1
        elif action == self.actionsMap['right']:
            col += 1
        return (row, col)

    def step(self, action):
        next_state = self.move(action)
        self.currentState = next_state

        # Handle reward
        if next_state == (1, 1):  # dead
            return next_state, -1, True
        elif next_state == (3, 3):  # goal
            return next_state, 10, True
        else:
            return next_state, -0.1, False
