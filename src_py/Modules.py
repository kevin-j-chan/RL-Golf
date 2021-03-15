# import
import random
import numpy as np
import matplotlib.pyplot as plt

# methods
# methods to create shapes for the golf course
def in_ellipse(x: int, y:int, a:int, b:int, rw:int, rh:int):
    return abs((x-a)**2 / rw**2 + (y-b)**2 / rh**2) <= 1
def in_rectangle(x: int, y:int, a:int, b:int, rw:int, rh:int):
    return x >= a - rw and x <= a + rw and y >= b - rh and y <= b + rh

# method that creates the golf course
#   returns
#       - list of possible states
#       - dict of state-action values
#       - dict of state rewards
#       - terminal states
def generate_course(width:int, height:int, n_actions:int, n_pits:int):
    # declare data structures
    S_out = []
    S_tout = []
    Q_out = dict()
    Map_out = dict()
    
    # initialize states, Q and R
    for y in range(height):
        for x in range(width):
            S_out.append( (y,x) )
            Q_out[(y,x)] = [0]*n_actions    
            Map_out[(y,x)] = 'O'             
    
    # randomly select hole for the goal and add it to terminal states
    hole = random.choice(S_out)
    S_tout.append(hole)

    # create various shapes on course for different point values
    random_shape = [random.choice([in_ellipse, in_rectangle]) for num in range(3)]
    for x in range(width):
        for y in range(height):
            if random_shape[0](y,x,hole[0],hole[1], 3,3):
                Map_out[(y,x)] = 'G'
            elif random_shape[1](y,x,hole[0],hole[1], 8,4):
                Map_out[(y,x)] = 'R'
            elif random_shape[2](y,x,hole[0],hole[1], HEIGHT * 3/4, WIDTH * 7/8):
                Map_out[(y,x)] = 'G'

    # set the hole coordinate to 'H'
    Map_out[hole] = 'H'
    
    # create sand pits
    cnt_pits = 0
    while cnt_pits < n_pits:
        pit = random.choice(S_out)
        locs = generate_pit_locations(Map_out, pit)
        if len(locs) > 0:
            cnt_pits += 1
        for l in locs:
            Map_out[l] = 'P'
    
    return S_out, S_tout, Q_out, Map_out

# method that creates the same course every time
def generate_test_course(width:int, height:int, n_actions:int, n_pits:int):
    # declare data structures
    S_out = []
    S_tout = []
    Q_out = dict()
    Map_out = dict()
    
    # initialize states, Q and Map
    for x in range(width):
        for y in range(height):
            S_out.append( (y,x) )
            Q_out[(y,x)] = [0]*n_actions    
            Map_out[(y,x)] = 'O'                
    
    # randomly select hole for the goal and add it to terminal states
    hole = (int(height / 2), int(width * 2/3))
    S_tout.append(hole)

    # create various shapes on course for different point values
    for x in range(width):
        for y in range(height):
            if in_ellipse(y,x,hole[0],hole[1], 3,3):
                Map_out[(y,x)] = 'G'
            elif in_rectangle(y,x,hole[0],hole[1], 8,4):
                Map_out[(y,x)] = 'R'
            elif in_rectangle(y,x,hole[0],hole[1], 9, 8):
                Map_out[(y,x)] = 'G'

    # set the hole coordinates
    Map_out[hole] = 'H'
    
    # create sand pits
    pits = [ (int(height/3), int(width/2)), (int(height * 3/4), int(width/2 + 3)), (int(height/2 - 2), int(width/2 + 2))]
    for pit in pits:
        locs = generate_pit_locations(Map_out, pit)
        for l in locs:
            Map_out[l] = 'P'
    
    return S_out, S_tout, Q_out, Map_out

# method to find start that is in valid terrain
def generate_start(Map:dict):
    start = random.choice(list(Map.keys()))
    while Map[start] == 'O' or Map[start] == 'H': 
        start = random.choice(list(Map.keys()))
    return start

def generate_pit_locations(Map, loc):
    ret = []
    if loc in Map.keys() and Map[loc] != 'H':
        ret.append(loc)
        for d in directions:
            if (loc[0]+d[0], loc[1]+d[1]) in Map.keys() and Map[(loc[0]+d[0], loc[1]+d[1])] != 'H':
                ret.append((loc[0]+d[0], loc[1]+d[1]))
    return ret

# print
# method that prints a formatted version of the golf course with rewards
def print_course(Map:dict):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = ""
            if Map[(y,x)] == 'G':
                color = CYAN
            elif Map[(y,x)] == 'R':
                color = GREEN
            elif Map[(y,x)] == 'H':
                color = RED
            else:
                color = BLACK
            print(color + Map[(y,x)], end=" ")
        print()

# method that prints a formatted version of the estimated values for each state, taking the maximum of all possible actions
def print_V(Q:dict):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = ""
            if Map[(y,x)] == 'G':
                color = CYAN
            elif Map[(y,x)] == 'R':
                color = GREEN
            elif Map[(y,x)] == 'H':
                color = RED
            else:
                color = BLACK

            if np.max(Q[(y,x)]) == 0:
                print(color + " 0.0", end=" ")
            else:
                print(color + str(np.round(np.max(Q[(y,x)]),1)), end=" ")
        print()

# method that prints a formatted version of the estimated values for each state, taking the maximum of all possible actions
def print_V_to_f(Q:dict, f):
    for x in range(WIDTH):
        for y in range(HEIGHT):

            if np.max(Q[(y,x)]) == 0:
                f.write(" 0.0 ")
            else:
                f.write(str(np.round(np.max(Q[(y,x)]),1)) + " ")
        f.write("\n")

# step
def step(start:tuple, strength:int, direction:tuple):  
    # check if in hole
    if Map[start] == 'H':
        return start, 0

    else:
        pos = [start[0], start[1]]
        # pits make the ball go significantly slower
        if Map[start] == 'P': 
            strength -= 2
        # rough patches make the ball go slower at starting position
        if Map[start] == 'R': 
            strength -= 1
        # ball moves in direction by one tick of strength
        for t in range(strength):
            newPos = [pos[0] + direction[0], pos[1] + direction[1]]
            # check if ball moves out of map. break, return last position and -1
            if tuple(newPos) not in S or Map[tuple(newPos)] == 'O':
                break
            # check if ball moves into sand pit or rough - if so, return previous state and reward
            elif Map[tuple(newPos)] == 'P':
                pos = newPos
                break
            # check if ball moves over goal - if so, return end state and reward
            elif Map[tuple(newPos)] == 'H':
                pos = newPos
                break
            # else ball keeps moving
            else:
                pos = newPos

        return tuple(pos), -1
