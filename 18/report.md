# Assignment 2 Part 2

1. Some of the interesting states were:
   1. For (N,2,2,R,25), IJ decides to go DOWN. However, from the more risky states where just the health of MM is more, eg, (N,2,2,R,50), IJ decides to CRAFT and remain safe from the attacks of MM
   2. From any state in east, IJ is always trying to hurt MM. However, from states like (E, 1, 0, D, 50), IJ decides to HIT in spite of having an arrow as the damage from the arrow can not end the game and he will have to ultimately HIT MM anyways. However, from (E, 1, 0, D, 25), IJ does SHOOT as it has a higher probability of success than HIT
   3. From (S,2,3,R,100), IJ decides to STAY instead of moving UP or GATHER as if STAY succeeds, IJ remains in South where he is safe from the attacks of MM. If STAY fails, IJ goes to East, where he has a high probability of hurting MM with the 3 arrows he has or HIT. The risk vs reward of the move seems better than the relative safety of GATHER in the state.
   4. From state (C,0,2,D,25), IJ decides to move RIGHT and have a higher chance of hitting MM.
   5. From West, IJ often tries to move to the RIGHT. However, there are some exceptions when MM is in Ready state. In those states, such as (W,1,2,R,75), IJ prefers to SHOOT, so that he remains safe from attacks by MM and also has a change of doing some damage to MM.
2. The trace file that we get for case 0 if consider the final policy of the value iteration algorithm, we can see some pattern that IJ should follow according to policy, depending on the state:
   1. If IJ is at position east, it tries to HIT or SHOOT MM since the probability of IJ damaging MM from East is high.
   2. The only time IJ tries to STAY at it's locations are when MM is in Ready state and IJ is not in Center or East. This helps IJ avoid attacks from MM as they only affect in Center or East. West has a particularly more of these as the probability of success of the action from West is 100%.
   3. If IJ is at location south, the policy decision to GATHER materials is less since to use the material to make arrows and then using the arrows to shoot at MM requires 6 time steps, which is depreciated due to the discount factor and STEP COST, so the policy is to move UP or STAY most of the times.
   4. Also when MM is in R state, IJ's policy is to be in locations where MM can't hit, but when MM is in D, IJ's policy is to move to locations from where IJ can HIT/SHOOT at MM.
   5. When MM's health is 25, IJ's policy is to SHOOT(if possible) and if MM's health is >50 then IJ's policy is to HIT, since SHOOT has high probability but less damage, and HIT has high damage but less probability.
3. The value iteration for the case 0 converges after 124 iterations of the algorithm, which is considerable since we have such high(close to 1) discount factor(gamma), as we decrease the gamma the number of iterations are reduced, as seen in case 3 where we keep the discount factor as 0.25 the iterations of value iteration algorithm is reduces to 9.
## Simulations

For ```(W, 0, 0, D, 100)```

IJ directly tries to go to East and HIT MM continuously from there. It leaves out the policies to GATHER and CRAFT as they require 5-6 more steps with a probability factor in  GATHER and moving too, making just directly hitting MM the better choice.

```
['W', 0, 0, 'D', 100]
RIGHT
['C', 0, 0, 'D', 100]
RIGHT
['E', 0, 0, 'D', 100]
HIT
['E', 0, 0, 'D', 100]
HIT
['E', 0, 0, 'D', 100]
HIT
['E', 0, 0, 'D', 100]
HIT
['E', 0, 0, 'D', 100]
HIT
['E', 0, 0, 'D', 100]
HIT
['E', 0, 0, 'D', 100]
HIT
['E', 0, 0, 'D', 100]
HIT
['E', 0, 0, 'D', 100]
HIT
['E', 0, 0, 'R', 100]
HIT
['E', 0, 0, 'R', 50]
HIT
['E', 0, 0, 'R', 50]
HIT
['E', 0, 0, 'D', 100]
HIT
['E', 0, 0, 'R', 50]
HIT
['E', 0, 0, 'R', 0]
exit    
Game over!

```

For ```(C, 2, 0, R, 100)```

Here, since IJ already had material, he tries to go UP and CRAFT arrows. In this simulation, that is successful. Then, as MM is in Ready state, IJ decides to STAY in North and wait till MM goes to Dormant state. Once that happens, IJ travels to East first, then just shoots and hits MM till the end of the game.

```
['C', 50, 0, 'R', 100]
UP
['N', 50, 0, 'R', 100]
CRAFT
['N', 1, 3, 'R', 100]
STAY
['N', 1, 3, 'D', 100]
DOWN
['C', 1, 3, 'D', 100]
RIGHT
['E', 1, 3, 'D', 100]
SHOOT
['E', 1, 50, 'D', 75]
SHOOT
['E', 1, 1, 'D', 50]
SHOOT
['E', 1, 0, 'D', 1]
HIT
['E', 1, 0, 'D', 0]
exit    
Game over!

```

## Case 1

These are no significant policy changes in this case

## Case 2

When in West, IJ does STAY in all cases and remains in West indefinitely. This is because as the step cost is now 0, the reward is maximized by just remaining the same place and not doing anything. The step cost of all the other actions is negative, except when IJ would attack and MM would die. However, the probability of that happening is so low that staying still remains beneficial.

## Case 3

In this case, value iteration takes just 9 iterations to complete, instead of 124 like when gamma was 0.999. This is because as the reward decreases substantially faster, the value iteration converges below the Bellman error significantly faster as well.

The policy obtained in this seems sub-optimal as compared to the policy obtained before. This is because IJ often times does non-risky things such as craft when he is at the state (N, 1, 0, D, 25). The previous policy recognized that given the step cost, it would be better to just go DOWN. However, this one still does CRAFT.

