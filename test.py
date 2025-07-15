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
        
        
env = Environment()
alpha = 0.1
gamma = 0.9
epsilon = 0.2
episodes = 1000

for ep in range(episodes):
    state = env.reset()
    done = False
    R = 0

    while not done:
        if state not in env.qtable:
            env.qtable[state] = { a: 0.0 for a in env.actionsMap.values() }

        # ε-greedy action selection
        if np.random.rand() < epsilon:
            action = np.random.choice(env.getValidActions(state))
        else:
            valid = { k: v for k, v in env.qtable[state].items() if k in env.getValidActions(state) }
            action = max(valid, key=valid.get)

        next_state, reward, done = env.step(action)
        R += reward

        if next_state not in env.qtable:
            env.qtable[next_state] = { a: 0.0 for a in env.actionsMap.values() }

        # Q-learning update
        print(state, env.getValidActions(state))
        env.qtable[state][action] = env.qtable[state][action] + alpha * (
            reward + gamma * max(env.qtable[next_state].values()) - env.qtable[state][action]
        )
        state = next_state
    
    print(f"episode: {ep}, reward: {R}")
    R = 0


grid = [['' for _ in range(4)] for _ in range(4)]

for r in range(4):
    for c in range(4):
        state = (r, c)
        if state == (1,1):
            grid[r][c] = 'x'
        elif state == (3,3):
            grid[r][c] = 'G'
        elif state in env.qtable:
            best_action = max(env.qtable[state], key=env.qtable[state].get)
            grid[r][c] = env.reverseActionsMap[best_action][0].upper()
        else:
            grid[r][c] = '?'

print("\nLearned Policy:")
print(tabulate(grid, tablefmt='grid'))

print(tabulate([k for k in env.qtable.values()]))
