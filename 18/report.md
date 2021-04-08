# Assignment 3

## PART 2
1. The trace file that we get for case 0 if consider the final policy of the value iteration algorithm, we can see some pattern that IJ should follow according to policy, depending on the state:
   1. If IJ is at position east, it tries to hit/shoot at MM since it is high probability that IJ damages MM at this location.
   2. When at position west, IJ tries to STAY at the same state, because at this location, if MM can't HIT IJ here and the actions planned 100 percent of the times.
   3. If IJ is at location south, the policy decision to GATHER materials is less since to use the material to make arrows and then using the arrows to shoot at MM requires 6 time steps, which is depreciated due to the discount factor and STEP COST, so the policy is to move UP or STAY most of the times.
   4. Also when MM is in R state, IJ's policy is to be in locations where MM can't hit, but when MM is in D, IJ's policy is to move to locations from where IJ can HIT/SHOOT at MM.
   5. When MM's health is 25, IJ's policy is to SHOOT(if possible) and if MM's health is >50 then IJ's policy is to HIT, since SHOOT has high probability but less damage, and HIT has high damage but less probability.
2. The value iteration for the case 0 converges after 124 iterations of the algorithm, which is considerable since we have such high(close to 1) discount factor(gamma), as we decrease the gamma the number of iterations are reduced, as seen in case 3 where we keep the discount factor as 0.25 the iterations of value iteration algorithm is reduces to 8.
## Simulations

For ```(W, 0, 0, D, 100)```

```
['W', '0', '0', 'D', '4']
RIGHT
['C', '0', '0', 'D', '4']
RIGHT
['E', '0', '0', 'D', '4']
HIT
['E', '0', '0', 'D', '4']
HIT
['E', '0', '0', 'D', '4']
HIT
['E', '0', '0', 'D', '4']
HIT
['E', '0', '0', 'D', '4']
HIT
['E', '0', '0', 'D', '4']
HIT
['E', '0', '0', 'D', '4']
HIT
['E', '0', '0', 'D', '4']
HIT
['E', '0', '0', 'D', '4']
HIT
['E', '0', '0', 'R', '4']
HIT
['E', '0', '0', 'R', '2']
HIT
['E', '0', '0', 'R', '2']
HIT
['E', '0', '0', 'D', '4']
HIT
['E', '0', '0', 'R', '2']
HIT
['E', '0', '0', 'R', '0']
exit    
Game over!

```

For ```(C, 2, 0, R, 100)```:

```
['C', '2', '0', 'R', '4']
UP
['N', '2', '0', 'R', '4']
CRAFT
['N', '1', '3', 'R', '4']
STAY
['N', '1', '3', 'D', '4']
DOWN
['C', '1', '3', 'D', '4']
RIGHT
['E', '1', '3', 'D', '4']
SHOOT
['E', '1', '2', 'D', '3']
SHOOT
['E', '1', '1', 'D', '2']
SHOOT
['E', '1', '0', 'D', '1']
HIT
['E', '1', '0', 'D', '0']
exit    
Game over!

```

