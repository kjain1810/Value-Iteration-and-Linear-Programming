import os

### Model (MDP problem)

class TransportationMDP(object):
    def __init__(self, N):
        # N = number of blocks
        self.N = N
        # 1 --> A
        # 2 --> B
        # 3 --> C
        # 4 --> D
    def startState(self):
        return 1
    def isEnd(self, state):
        return state == self.N
    def actions(self, state):
        # return list of valid actions
        result = []
        if state == 1:
            result.append('right') # +1
            result.append('up') # +2
        if state == 2:
            result.append('left') # -1
            result.append('up') # +2
        if state == 3:
            result.append('down') # -2
            result.append('right') # +!
        return result
    def succProbReward(self, state, action):
        # return list of (newState, prob, reward) triples
        # state = s, action = a, newState = s'
        # prob = T(s, a, s'), reward = Reward(s, a, s')
        result = []
        if state == 1:
            if action == 'up':
                result.append((3, 0.8, -1))
            else:
                result.append((2, 0.8, -1))
            result.append((1, 0.2, -1))
        if state == 2:
            if action == 'up':
                result.append((4, 0.8, -4))
            else:
                result.append((1, 0.8, -1))
            result.append((2, 0.2, -1))
        if state == 3:
            if action == 'right':
                result.append((4, 0.25, -3))
                result.append((3, 0.75, -1))
            else:
                result.append((1, 0.8, -1))
                result.append((3, 0.2, -1))
        return result
    def discount(self):
        return 1.
    def states(self):
        return range(1, self.N+1)

# Inference (Algorithms)

def valueIteration(mdp):
    # initialize
    V = {} # state -> Vopt[state]
    for state in mdp.states():
        V[state] = 0.

    def Q(state, action):
        return sum(prob*(reward + mdp.discount()*V[newState]) \
                for newState, prob, reward in mdp.succProbReward(state, action))

    while True:
        # compute the new values (newV) given the old values (V)
        newV = {}
        for state in mdp.states():
            if mdp.isEnd(state):
                newV[state] = 0.
            else:
                newV[state] = max(Q(state, action) for action in mdp.actions(state))
        # check for convergence
        if max(abs(V[state]-newV[state]) for state in mdp.states())<1e-10:
            break
        V = newV

        # read out policy
        pi = {}
        for state in mdp.states():
            if mdp.isEnd(state):
                pi[state] = 'none'
            else:
                pi[state] = max((Q(state, action), action) for action in mdp.actions(state))[1]

        # print stuff out
        os.system('clear')
        print('{:20} {:20} {:20}'.format('s', 'V(s)', 'pi(s)'))
        for state in mdp.states():
            print('{:20} {:20} {:20}'.format(state, V[state], pi[state]))
        input()


mdp = TransportationMDP(N=4)
#print(mdp.actions(3))
#print(mdp.succProbReward(3, 'walk'))
#print(mdp.succProbReward(3, 'tram'))
valueIteration(mdp)
