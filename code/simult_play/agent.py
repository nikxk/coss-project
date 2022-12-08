from random import choice

class Agent:

    # This class defines a player which can take part in a game, with certain discrete actions and a cost that is incurred, based on the actions of all the players of the game.

    def __init__(self, actions):
        self.action = choice(actions)
        self.all_actions = actions
        self.action_history = [self.action]
        self.turns = []
        self.cost_history = []
        self.accumulated_cost = 0

    def take_action(self, costs, turn = -1):
        self.action, cost = min(costs.items(), key=lambda x: x[1])
        self.turns.append(turn)
        self.action_history.append(self.action)

    def receive_cost(self, cost):
        self.accumulated_cost += cost
        self.cost_history.append(cost)
        self.cost = cost