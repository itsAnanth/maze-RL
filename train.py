env = Environment()
alpha = 0.1
gamma = 0.9
epsilon = 0.2
episodes = 500

for ep in range(episodes):
    state = env.reset()
    done = False

    while not done:
        if state not in env.qtable:
            env.qtable[state] = { a: 0.0 for a in env.actionsMap.values() }

        # ε-greedy action selection
        if np.random.rand() < epsilon:
            action = np.random.choice(env.getValidActions(state))
        else:
            action = max(env.qtable[state], key=env.qtable[state].get)

        next_state, reward, done = env.step(action)

        if next_state not in env.qtable:
            env.qtable[next_state] = { a: 0.0 for a in env.actionsMap.values() }

        # Q-learning update
        env.qtable[state][action] += alpha * (
            reward + gamma * max(env.qtable[next_state].values()) - env.qtable[state][action]
        )

        state = next_state


grid = [['' for _ in range(4)] for _ in range(4)]

for r in range(4):
    for c in range(4):
        state = (r, c)
        if state == (1,1):
            grid[r][c] = 'D'
        elif state == (3,3):
            grid[r][c] = 'G'
        elif state in env.qtable:
            best_action = max(env.qtable[state], key=env.qtable[state].get)
            grid[r][c] = env.reverseActionsMap[best_action][0].upper()
        else:
            grid[r][c] = '?'

print("\nLearned Policy:")
print(tabulate(grid, tablefmt='grid'))
