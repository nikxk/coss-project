import numpy as np

class Actions:
    ''' 
    actions.last() returns the last action taken by the agent.
    actions.next(action) updates the history of actions taken by the agent with the next action
    '''
    def __init__(self, actions):
        self.all_actions = actions
        self.history = [np.random.randint(len(actions))]
        self.last_iter = self.history[-1]
    
    def next(self, action):
        self.history.append(action)

    def last(self):
        return self.last_iter
    
    def next_iter(self, action):
        self.last_iter = action

class Costs:
    '''
    costs.last() returns the last cost incurred by the agent.
    costs.receive(cost) updates the history of costs incurred by the agent with the next cost
    '''
    def __init__(self):
        self.reset()
        self.last_iter = 0

    def receive(self, cost):
        self.accumulated += cost
        self.history.append(cost)

    def last(self):
        return self.history[-1]

    def reset(self):
        self.history = []
        self.accumulated = 0

class Agent:
    def __init__(self, actions, cost_setup, gamma=None):
        self.actions = Actions(actions)
        self.costs = Costs()
        self.cost_ferry, self.cost_alley, self.cost_alley_mult, _ = cost_setup

        self.gamma = np.random.rand() if gamma is None else gamma
        self.last_turn = 0
        self.neighbours = []

    def _update_number_playing(self, action):
        '''returns the change in state numbers if agent plays action'''
        return np.array([[1,0], [0,1], [0,0], [1,1]])[action]

    def own_cost_playing(self, action, state):
        '''cost incurred by agent playing action at given state'''
        n_BD, n_AC = state
        if action == 0:
            return self.cost_ferry + self.cost_alley + self.cost_alley_mult * n_BD
        elif action == 1:
            return self.cost_ferry + self.cost_alley + self.cost_alley_mult * n_AC
        elif action == 2:
            return 2 * self.cost_ferry
        elif action == 3:
            return 2 * self.cost_alley + self.cost_alley_mult * (n_BD + n_AC)

    def own_cost(self, state):
        '''cost incurred by agent by playing chosen action at given state'''
        return self.own_cost_playing(self.actions.last(), state)

    def neighbour_cost(self, state):
        '''cost incurred by agent's neighbours by playing their respective chosen actions at given state'''
        return sum([neighbour.own_cost(state) for neighbour in self.neighbours]) if self.neighbours else 0

    def take_action(self, state):
        '''agent takes action in iteration based on state'''

        # exclude agent from current state numbers
        new_state = -self._update_number_playing(self.actions.last()) + state

        # calculate the cost incurred if the agent takes a certain action (accounting for how the state numbers change afterwards)
        g = self.gamma
        n = len(self.neighbours)+1

        n_if_play_action = [self._update_number_playing(action) + new_state for action in range(4)]

        costs = [
            self.own_cost_playing(action, state) + g * self.neighbour_cost(state)
            if n!=0 else self.own_cost_playing(action, state) for action, state in enumerate(n_if_play_action)]

        # take the action with the lowest cost
        action = np.argmin(costs)
        self.actions.next_iter(action)

        return new_state + self._update_number_playing(action)
