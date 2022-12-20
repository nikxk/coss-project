import numpy as np
from agent import Agent
from tqdm import tqdm

class CongestionGame:
    '''
    The game class. Initializes the agents according to parameters passed on.
    cost_setup: tuple of (\alpha, \beta, \gamma, NE without bridge)
    agent_setup: tuple of (n_neighbours, gamma)
    
    play() runs the game and stores the results.
    run_history stores the results of each stage of the game. For each stage, it stores:
        - the number of iterations it took to converge
        - the number of agents taking each of the four actions
        - the average cost for each agent in the stage
        - the gamma, number of neighbours and cost incurred for each agent in the stage
    '''
    def __init__(self, n_agents=60, cost_setup=(15, 2, 0.2, 23), agent_setup=(None, None), order=None, intelligent=False):
        self.actions = ['ABD', 'ACD', 'ABCD', 'ACBD']
        self.cost_setup = cost_setup
        self.intelligent = intelligent
        self.n_BD, self.n_AC = 0, 0

        self._init_agents(n_agents, agent_setup)
        self._iter_reorder = order
        self.stage, self.iteration = 0, 0
        self.run_history = []
        
    def _init_agents(self, n_agents, agent_setup):
        '''initializes agents and sets number taking BD and AC paths'''
        self.n_agents = n_agents
        n_neighbours, gamma = agent_setup
        self.agents = [Agent(self.actions, self.cost_setup, gamma) for _ in range(n_agents)]
        self._update_numbers()

        if n_neighbours is None:
            n_neighbours = np.random.randint(0, n_agents)
        self._set_neighbours(n_neighbours)

    def _update_numbers(self):
        '''updates number taking BD and AC paths'''
        last_actions = [agent.actions.last() for agent in self.agents]

        num_of = lambda action: last_actions.count(self.actions.index(action))
        self.n_BD = num_of('ABD') + num_of('ACBD')
        self.n_AC = num_of('ACD') + num_of('ACBD')
    
    def _set_neighbours(self, n_neighbours):
        '''sets neighbours for each agent assuming agents are in a circle'''
        for i, agent in enumerate(self.agents):
            agent.neighbours = [self.agents[(i + j) % self.n_agents] for j in range(1, n_neighbours + 1)]

    def set_neighbours_individual(self, agent, n_neighbours):
        '''sets neighbours for a single agent'''
        i = self.agents.index(agent)
        agent.neighbours = [self.agents[(i + j) % self.n_agents] for j in range(1, n_neighbours + 1)]

    def _num_agents_taking_action(self):
        '''returns number of agents taking each action'''
        actions = [agent.actions.last() for agent in self.agents]
        return [actions.count(action) for action in range(4)]

    def play(self, n_stages=1, n_iterations=1, verbose=True):
        '''plays the game for n_stages and n_iterations'''

        stage_iter = tqdm(range(n_stages)) if verbose else range(n_stages)

        for _ in stage_iter:
            self.stage += 1
            self.iteration = 0
            for _ in range(n_iterations):
                self.iteration += 1
                last_actions = self._num_agents_taking_action()

                # decide order of playing
                if self._iter_reorder is not None:
                    self._iter_reorder(self.agents)

                # take actions
                for turn, agent in enumerate(self.agents):
                    agent.last_turn = turn
                    self.n_BD, self.n_AC = agent.take_action([self.n_BD, self.n_AC])

                # update costs within iteration, to decide ordering for next iteration
                for agent in self.agents:
                    agent.costs.last_iter = agent.own_cost([self.n_BD, self.n_AC])

                # check if converged (not exactly, but close enough)
                if self._num_agents_taking_action() == last_actions:
                    break
            
            # record the action taken by each agent
            for agent in self.agents:
                agent.actions.next(agent.actions.last())

            # update state numbers according to the action taken
            self._update_numbers()

            # record the cost for each agent
            stage_cost = 0
            for agent in self.agents:
                cost = agent.own_cost([self.n_BD, self.n_AC])
                agent.costs.receive(cost)
                stage_cost += cost
            
            # update gamma and neighbours for next stage
            if self.intelligent:
                for agent in self.agents:
                    if agent.costs.last() > self.cost_setup[-1]:
                        agent.gamma = agent.gamma/4.0
                        self.set_neighbours_individual(agent, max(0, len(agent.neighbours)//4))
                    else:
                        agent.gamma = min(1, agent.gamma*2.0)
                        self.set_neighbours_individual(agent, int(min(self.n_agents, len(agent.neighbours)*2)))
            
            self.run_history.append([self.iteration, self._num_agents_taking_action(), stage_cost/self.n_agents, [[agent.gamma, len(agent.neighbours), agent.costs.last()] for agent in self.agents]])