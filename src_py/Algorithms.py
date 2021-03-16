exec(open("Modules.py").read())
exec(open("Variables_Constants.py").read())

def epsilon_greedy(Q, state):
    be_greedy = np.random.random() < 1 - EPSILON
    if be_greedy: 
        action = np.argmax(Q[state])
    else:                            
        action = np.random.randint(0, n_actions)
    
    s = int(action / len(directions))  # 0 is PUTT, 1 is DRIVER
    d = action % len(directions)     
    return s, d

tar_dir = "../output/"
tar_name = "q_learning"
for it in iterations:
    f = open(tar_dir + tar_name + "_" + str(it) + ".txt", 'w')
    S, S_t, Q, Map  = generate_test_course(WIDTH, HEIGHT, n_actions, NUM_SAND_PITS) 
    # Loop through 'it' number of episodes
    for i in range(it):
        state = generate_start(Map)
        # Loop for each step of episode
        while state not in S_t:
            s, d = epsilon_greedy(Q, state)
            newState, reward = step(state, strengths[s], directions[d])
            Q[state][s * len(directions) + d] = Q[state][s * len(directions) + d] + ALPHA * (reward + GAMMA * max(Q[newState]) - Q[state][s * len(directions) + d])
            state = newState 
    f.write("iteration : " + str(it) + "\n")
    print_V_to_f(Q, f)
    f.write("\n")
    f.close()

tar_dir = "../output/"
tar_name = "dyna_q"
n_planning_steps = 40

for it in iterations:
    f = open(tar_dir + tar_name + "_" + str(it) + ".txt", 'w')
    S, S_t, Q, Map  = generate_test_course(WIDTH, HEIGHT, n_actions, NUM_SAND_PITS) 
    model = dict()
    for s in S:
        for a in range(len(strengths)):
            for d in range(len(directions)):
                model[s,a,d] = None
    # Loop for each episode
    for i in range(it):
        # Get random state and action by policy
        state = generate_start(Map)
        s, d = epsilon_greedy(Q, state)
        # Take action A
        state_next, reward = step(state, strengths[s], directions[d])
        # Update Q
        Q[state][s * len(directions) + d] = Q[state][s * len(directions) + d] + ALPHA * (reward + GAMMA * max(Q[state_next]) - Q[state][s * len(directions) + d])
        # Store the transition in your model array
        model[state, s, d] = state_next, reward

        for k in range(n_planning_steps):
            # random previously observed state
            state_p = random.choice(S)
            while np.min(Q[state_p]) == 0:
                state_p = random.choice(S)

            # we want to pick a random previously observed action
            action_p_idx = random.choice([i for i in range(n_actions) if Q[state][i] != 0])
            
            s_p = int(action_p_idx / len(directions)) 
            d_p = action_p_idx % len(directions)

            state_next_p, reward_p = step(state_p, strengths[s_p], directions[d_p])
            model[state_p, s_p, d_p] = state_next_p, reward_p

            Q[state_p][s_p * len(directions) + d_p] = Q[state_p][s_p * len(directions) + d_p] + ALPHA * (reward_p + GAMMA * max(Q[state_next_p]) - Q[state_p][s_p * len(directions) + d_p])
    f.write("iteration : " + str(it) + "\n")
    print_V_to_f(Q, f)
    f.write("\n")
    f.close()