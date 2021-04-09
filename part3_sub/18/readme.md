# Assignment 2 Part 3

## A matrix

We first start by creating a matrix of dimension 1936 x 600, where 1936 are number of state-action pairs and 600 is the number of states.

Our matrix will have a row for each of the state-action pair. In each of these rows, for states that are not end states, the value of the next states index will be -(probability of reaching that state) while the value of the current state index will be (probability of going to a different state). For end states, the value of the current state index will be 1. All the rest in both the cases will be 0. This ensures that the flow from the end state is 1 and the flow from all the other states is 0.

## R vector

The reward for each state-action pair is the expected reward of taking that action, ie, the weighted sum of reward in all of the possible next states.

For end states, the reward will be 0, as specified in the question

## Finding the policy

We first enumerated all of our states from 0 to 600.

After that, we kept a track of the number of state-action pair from each of the states that we encounter. We also store which row corresponds to which action from the state.

Suppose a state's pairs were occupied the ith to the jth rows. The resultant X vector from our LP would contain the expected rewards in the ith to the jth indices. Taking the argmax from this range would give us the best action from our current state.

We can find the policy by doing this for all states.

## Multiple policies

Yes, there can be multiple policies as

1. We can change our alpha matrix to start from some other state or even have a probabilistic start. This would change our policy
2. The order in which we consider our states and actions right now affect what the policy is turning out to be.
3. Changing the definition of argmax to take the first maximum argument instead of the last or vice versa will have an effect on our policy.