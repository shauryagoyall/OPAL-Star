## model.py 

has a whole code block for opal policy. this is the clone of the policy object with some minor modifications.

it is initialized with 2 categorical distributions corresponding to 2 actors (self.dist1 and self.dist2)

act function is split into 2 sub functions - act and act_other

act function - combines the probabilities from both these distributions to a categorical distribution that is used to sample the action. both probabilities weighed by 0.5

action is converted to [[a1], [a2] ...] form from [a1, a2 ...]

only the action is returned from this act function which is moved to GPU in the main.py file

act_other - uses the action tensor on gpu to return log probs, entropies etc

evaluate_actions - returns 2 log probs, 2 entropies as there are 2 distributions

## storage.py

added arrays, option to move array to GPU/CPU for action_log_probs 2

2 types of insert functions- opal_insert and insert
opal_insert is used by opal_policy as 2 actors and insert for all other algorithms

opal_insert - option to insert action_log_probs2

## arguments.py

modified slightly to include opal algorithm