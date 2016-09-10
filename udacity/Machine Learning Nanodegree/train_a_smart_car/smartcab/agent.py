import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env, gamma = 0.8, epsilon = 0.1):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
	self.alpha = 0.0
	self.alpha_called = 0
	self.gamma = gamma
	self.epsilon = epsilon
        # TODO: Initialize any additional variables here

	### Two Variables. Prev_state and next_state/current_state
	self.prev_reward = 0
	self.state = None
	self.prev_state = ('forward', 'red', 'forward', 0)
	self.prev_action = None

	### initializing q values as dictionary of dictionary
	self.q = dict()
	for self.next_waypoint in ['right', 'left', 'forward', None]:
		for in_light in ['red', 'green']:
			for in_oncoming in ['forward', 'right', 'left', None]: 
				for in_left in [0, 1]:
					state = (self.next_waypoint, in_light, in_oncoming, in_left)
					self.q[state] = dict()
					self.q[state]['forward'] = 0.04
					self.q[state]['left'] = 0.03
					self.q[state]['right'] = 0.02
					self.q[state][None] = 0.01

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update_learn(self):
	self.alpha_called += 1
	self.alpha = 1.0/math.log(self.alpha_called + 16, 16)

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

	## Random actions
        #action = random.choice(self.env.valid_actions[0:])
        #reward = self.env.act(self, action)

        # TODO: Update state

	## The following states are used:
	## inputs['light'] = 'red' or 'green'
	## inputs['oncoming'] = 'forward', 'right', or 'left' or None
	## inputs['left'] = 1 means 'forward', 0 means 'left' or 'right'

	in_light = inputs['light']
	in_oncoming = inputs['oncoming']
	in_left = int(inputs['left'] == 'forward')
	self.state = (self.next_waypoint, in_light, in_oncoming, in_left)

        
        # TODO: Select action according to your policy

	## Find the action that has the max q-value in the current state
	action = None
	max_action = 0.0
	for action_t in self.q[self.state]:
		if (self.q[self.state][action_t] > max_action):
			max_action = self.q[self.state][action_t]
			action = action_t


	## with 10% probability select a random action and 90% use the action that has max q value in the current state.
	if ( random.randrange(0, 100, 1) > ((1 - self.epsilon) * 100) ):
		#print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Overrode Action  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
		action = random.choice(self.env.valid_actions[0:])

		
        # Execute action and get reward
        reward = self.env.act(self, action)
	

        # TODO: Learn policy based on state, action, reward
	## We have implented q-learning algorithm here because we choose the action that provides the maximum q-value irrespective of what action
	## that will actually be taken in the next state. While in SARSA the actual action taken is observed and used in equation

	## SARSA:
 	## Q(s,a) <- Q(s,a) + alpha*[r + gamma*Q(s',a') - Q(s,a)]
	## Q-Learning:
 	## Q(s,a) <- Q(s,a) + alpha*[r + gamma* max'_a Q(s',a') - Q(s,a)]

	max_action = 0.0
	for action_t in self.q[self.state]:
		if (self.q[self.state][action_t] > max_action):
			max_action = self.q[self.state][action_t]


	self.q[self.prev_state][self.prev_action] = ((1 - self.alpha)* self.q[self.prev_state][self.prev_action]) + self.alpha * (self.prev_reward + self.gamma * max_action)

	self.prev_reward = reward
	self.prev_state = self.state
	self.prev_action = action	

	#print self.q

	#print self.alpha_called	
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}, alpha = {}".format(deadline, inputs, action, reward, self.alpha)  # [debug]


def run():
	"""Run the agent for a finite number of trials."""
	
	# Set up environment and agent
	e = Environment()  # create environment (also adds some dummy traffic)
	result = dict()
	#for gamma in range(6,9,1):
	#	gamma *= 0.1	
	for gamma in [0.6]:
		result[gamma] = dict()
		#for epsilon in range(5,15,5):
		#	epsilon *= 0.01
		for epsilon in [0.05]:
			a = e.create_agent(LearningAgent, gamma, epsilon)  # create agent
			#e.set_primary_agent(a, enforce_deadline=False)  # specify agent to track
			e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
			# NOTE: You can set enforce_deadline=False while debugging to allow longer trials
	
			# Now simulate it
			sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
			# NOTE: To speed up simulation, reduce update_delay and/or set display=False
	
			sim.run(n_trials=100)  # run for a specified number of trials
			#sim.run(n_trials=10)  # run for a specified number of trials
			# NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

			print "\n\n\n\nCorrect results are:",
			print a.env.correct
			print "\n\n\n\n"
			result[gamma][epsilon] = a.env.correct	


	print "gamma", "epsilon", "% reached"
	for gamma in result:
		for epsilon in result[gamma]:
			print gamma, epsilon, result[gamma][epsilon]

	#print "\n\n\n\nState   ", "Action    ", "    Values"
	#for state in a.q:
	#	for action in a.q[state]:
	#		print state, action, a.q[state][action]
		
		


if __name__ == '__main__':
    run()
