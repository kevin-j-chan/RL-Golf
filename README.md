# RL-Golf
This project uses reinforcement learning to find the optimal stroke count for a game of golf. We run Q-Learning and Dyna-Q methods on a designed golf environment, exploring the states and actions with an e-greedy (*e* = 0.1) policy. By running these methods against each other on the same environment, we can see how quickly these methods converge to an optimal solution, and whether or not the model-based planning method is helpful in small, concrete environments. 

## How to run
Download the repository and ensure that the **random**, **numpy**, and **matplotlib** libraries are supported.
### For Jupyter Notebook
Navigate to the **src** directory and run all cells in the Algorithms notebook. Output shall be printed inside the notebook.
### For Python
Navigate to the **src_py** directory and run the Algorithms file. Output shall be written into the **output** directory.
The outputs are written into individual text files because it allows us to more easily compare the outputs, using commands like **diff** in the terminal.

## Environment
Our golf environment is composed in a 2D array for WIDTH * HEIGHT, where the states are programatically determined. Each state is assigned a possible value, ['O', 'R', 'G', 'H', 'P'] and each state has a distinctive property:
* O is Out. Out cannot be reached, so running into this state will return the state to a previous one and end the action
* R is Rough. Rough represents a rugged golf terrain, which will modify the action by distance - 1.
* G is Green. Green is a standard golf terrain, which does nothing to the action.
* H is Hole. Hole is the terminal state, which ends each episode.
* P is (Sand) Pit. Sand pits are heavy modifiers that modify the action by distance - 2.

There are two methods that generate environments.
* generate_course -> this creates a randomly generated golf course by selecting a place for the end state (the hole) and generating shapes around it
* generate_test_course -> this creates the same golf course every time

Our actions consist of strength and direction. There are two possible strengths based on which tool is used (PUTT = 2 distance, DRIVER = 3 distance). As you can see, the PUTT strength will not be able to remove the agent from the sand pits with the -2 modifier. The possible directions are up, down, left and right. The code can easily be adjusted to add more directions and strengths in the Variables_Constants file.

## Algorithms
As mentioned earlier, we will be using both Q-Learning and Dyna-Q methods against our environment.
For both methods, we are considering:
* EPSILON = 0.1, which means there is a 10% chance to explore a random action
* ALPHA = 0.1, which is our step-size parameter that influences the rate of learning
* GAMMA = 1, which is because our task is not discounted

For Dyna-Q, we also have:
* n_planning_steps = 100, for purpose of testing, we have 100 planned steps.

## Examples
Here are some examples of the converging state estimates - you will also see these as outputs in the Jupyter Notebook.

This is a text visualization of our state map.

![Figure 1: Test Course](images/test_course.PNG)

Here is Q-Learning ran up against the environment, converging at 50,000 iterations.

![Figure 2: Q-Learning, fully converged at 50000 iterations](images/q_learning_25000_50000.PNG)

Here is Dyna-Q ran up against the same environment, converging at 10,000 iterations with n_planning_steps = 100.

![Figure 3: Dyna-Q, fully converged at 10000 iterations](images/dyna_q_10000.PNG)
