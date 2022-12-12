from agent import Agent

class CongestionGameNoBridge:

    def arrange_players(self):
        '''sort players in the order they decide on actions'''
        # players who waited longer go first
        self.players.sort(key=lambda x: x.accumulated_cost, reverse=True)

    def exp_player_costs(self):
        '''costs for a player if they take an action'''
        return {
            'ABD': self.cost_ferry + self.cost_alley + self.cost_alley_mult * (self.n_BD + 1) , 
            'ACD': self.cost_ferry + self.cost_alley + self.cost_alley_mult * (self.n_AC + 1) }
            
    def play(self, rounds = 1, till_convergence = False):
        for _ in range(rounds):
            if self.is_converged and till_convergence:
                break

            self.iterations += 1
            old_n = self.n_AC, self.n_BD

            # order players so ones with higher accumulated cost decide first
            self.arrange_players()

            # players decide on actions
            for idx, player in enumerate(self.players):

                # change numbers so previous player action not included
                self._update_numbers(player.action, -1)

                # let player take action
                player.take_action(costs = self.exp_player_costs(), turn = idx)

                # include player in numbers
                self._update_numbers(player.action)

            # now that actions are decided, fix the costs
            costs_fixed = self.costs()

            # assign individual costs to players
            for player in self.players:
                player.receive_cost(costs_fixed[player.action])

            if old_n == (self.n_AC, self.n_BD):
                self.is_converged = True

    def costs(self): 
        '''costs for a player already decided on an action'''
        return {
            'ABD': self.cost_ferry + self.cost_alley + self.cost_alley_mult * self.n_BD , 
            'ACD': self.cost_ferry + self.cost_alley + self.cost_alley_mult * self.n_AC }

    def __init__(self, n_players=60, cost_setup=(15, 2, 0.2)):
        self.cost_ferry, self.cost_alley, self.cost_alley_mult = cost_setup
        self.actions = ['ABD', 'ACD']
        self._initialize_players(n_players)

        self.iterations = 0
        self.is_converged = False

    def _initialize_players(self, n_players):
        self.players = [Agent(actions = self.actions) for _ in range(n_players)]
        acts = [player.action for player in self.players]
        self.n_AC, self.n_BD = acts.count('ACD'), acts.count('ABD')

    def _update_numbers(self, action, add = 1):
        ''' Updates the number of people on each path. '''
        if action == 'ABD':
            self.n_BD += add
        elif action == 'ACD':
            self.n_AC += add




class CongestionGameBridge:

    def arrange_players(self):
        '''sort players in the order they decide on actions'''
        # players who waited longer go first
        self.players.sort(key=lambda x: x.accumulated_cost, reverse=True)

    def exp_player_costs(self, idx):
        '''costs expected for a player if they take an action (assuming they take the action with some decided and others playing previous action). This player is currently not included in the numbers.'''
        new_costs = {}

        # ABD
        self.n_BD += 1
        new_fixed_cost = self.costs()
        others_costs = sum([new_fixed_cost[player.action] for player in self.players]) - new_fixed_cost[self.players[idx].action]
        new_costs['ABD'] = new_fixed_cost['ABD'] + self.gamma * others_costs
        self.n_BD -= 1

        # ACD
        self.n_AC += 1
        new_fixed_cost = self.costs()
        others_costs = sum([new_fixed_cost[player.action] for player in self.players]) - new_fixed_cost[self.players[idx].action]
        new_costs['ACD'] = new_fixed_cost['ACD'] + self.gamma * others_costs
        self.n_AC -= 1

        # ABCD
        new_fixed_cost = self.costs()
        others_costs = sum([new_fixed_cost[player.action] for player in self.players]) - new_fixed_cost[self.players[idx].action]
        new_costs['ABCD'] = new_fixed_cost['ABCD'] + self.gamma * others_costs

        # ACBD
        self.n_AC += 1
        self.n_BD += 1
        new_fixed_cost = self.costs()
        others_costs = sum([new_fixed_cost[player.action] for player in self.players]) - new_fixed_cost[self.players[idx].action]
        new_costs['ACBD'] = new_fixed_cost['ACBD'] + self.gamma * others_costs
        self.n_AC -= 1
        self.n_BD -= 1

        return new_costs

    def play(self, rounds = 1, till_convergence = False):
        for _ in range(rounds):
            if self.is_converged and till_convergence:
                break

            self.iterations += 1
            old_n = self.n_AC, self.n_BD, [player.action for player in self.players].count('ACBD')

            # order players so ones with higher accumulated cost decide first
            self.arrange_players()

            # players decide on actions
            for idx, player in enumerate(self.players):

                # change numbers so previous player action not included
                self._update_numbers(player.action, -1)

                # let player take action
                player.take_action(costs = self.exp_player_costs(idx), turn = idx)

                # include player in numbers
                self._update_numbers(player.action)

            # now that actions are decided, fix the costs
            costs_fixed = self.costs()

            # assign individual costs to players
            for player in self.players:
                player.receive_cost(costs_fixed[player.action])

            if old_n == (self.n_AC, self.n_BD, [player.action for player in self.players].count('ACBD')):
                self.is_converged = True
            
    def costs(self): 
        '''costs for a player already decided on an action'''
        return {
            'ABD': self.cost_ferry + self.cost_alley + self.cost_alley_mult * self.n_BD , 
            'ACD': self.cost_ferry + self.cost_alley + self.cost_alley_mult * self.n_AC ,
            'ABCD': 2 * self.cost_ferry ,
            'ACBD': 2 * self.cost_alley + self.cost_alley_mult * (self.n_AC + self.n_BD)}

    def __init__(self, n_players=60, cost_setup=(15, 2, 0.2), gamma=0):
        self.cost_ferry, self.cost_alley, self.cost_alley_mult = cost_setup
        self.actions = ['ABD', 'ACD', 'ABCD', 'ACBD']
        self._initialize_players(n_players)

        self.gamma = gamma
        self.iterations = 0
        self.is_converged = False

    def _initialize_players(self, n_players):
        self.players = [Agent(actions = self.actions) for _ in range(n_players)]
        acts = [player.action for player in self.players]
        self.n_AC = acts.count('ACD') + acts.count('ACBD')
        self.n_BD = acts.count('ABD') + acts.count('ACBD')

    def _update_numbers(self, action, add = 1):
        ''' Updates the number of people on each path. '''
        if action == 'ABD':
            self.n_BD += add
        elif action == 'ACD':
            self.n_AC += add
        elif action == 'ACBD':
            self.n_AC += add
            self.n_BD += add



# Legacy:

# class CongestionGame:
#     '''
#     Defines a congestion game where the players are pedestrians who want to get from node A to node D. They pass through nodes B and C in between. A-B and C-D are waterways, A-C and B-D are alleys. There is a bridge between B and C which may or may not be connected. Time taken on the waterway is high and fixed and on alleys it is proportional to the number of people using it.

#     __Parameters__
#     has_bridge : bool
#         Whether the bridge is connected or not.

#     __Functions__
#     play(rounds)
#         Plays the game for a number of rounds.
#     connect_bridge()
#         Connects the bridge.
        
#     __to edit__
#     arrange_players()
#         Defines how the players are arranged before each round.

#     '''

#     def arrange_players(self):
#         # players who waited longer to go first
#         self.players.sort(key=lambda x: x.accumulated_cost, reverse=True)

#     def play(self, rounds = 1):
#         for _ in range(rounds):
#             self.arrange_players()
#             for idx, player in enumerate(self.players):
#                 self.update_numbers(player.prev_actions[-1], -1)
#                 action = player.take_action(costs = self.costs, turn = idx)
#                 self.update_numbers(action)
#                 self.update_costs()

#     def __init__(self, n_players=60, has_bridge=False, cost_setup=(15, 2, 0.2)):
#         # setting up the game
#         self.has_bridge = has_bridge
#         self.cost_ferry, self.cost_alley, self.cost_alley_mult = cost_setup
#         self.n_AC, self.n_BD = 0, 0
#         self.initialize_actions()

#         # setting up the players
#         self.initialize_players(n_players)

#     def initialize_actions(self):
#         self.actions = ['ABD', 'ACD']
#         self.costs = {
#             'ABD': self.cost_ferry + self.cost_alley + self.cost_alley_mult * self.n_BD,
#             'ACD': self.cost_ferry + self.cost_alley + self.cost_alley_mult * self.n_AC }
#         if self.has_bridge:
#             self.actions.append('ABCD')
#             self.actions.append('ACBD')
#             self.costs['ABCD'] = 2 * self.cost_ferry
#             self.costs['ACBD'] = 2 * self.cost_alley + self.cost_alley_mult * (self.n_AC+self.n_BD)

#     def initialize_players(self, n_players):
#         self.players = [Agent(actions = self.actions) for _ in range(n_players)]
#         for player in self.players:
#             action = player.take_first_action()
#             self.update_numbers(action)
#         self.update_costs()

#     def connect_bridge(self):
#         self.has_bridge = True
#         for player in self.players:
#             player.actions = self.actions
#         self.initialize_actions()

#     def update_costs(self):
#         self.costs['ABD'] = self.cost_ferry + self.cost_alley + self.cost_alley_mult * self.n_BD
#         self.costs['ACD'] = self.cost_ferry + self.cost_alley + self.cost_alley_mult * self.n_AC
#         if self.has_bridge:
#             self.costs['ACBD'] = 2 * self.cost_alley + self.cost_alley_mult * (self.n_AC+self.n_BD)

#     def update_numbers(self, action, add = 1):
#         if action == 'ABD':
#             self.n_BD += add
#         elif action == 'ACD':
#             self.n_AC += add
#         elif action == 'ACBD':
#             self.n_AC += add
#             self.n_BD += add