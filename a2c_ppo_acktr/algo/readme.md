## opal.py

calls evaluate_action from opal_policy

computes action loss 2 for the 2nd distribution using the action that was sampled after combining both distribution probabilities

loss includes + action_loss2 and - (distribution_entropy_2 * scaling factor)

modified return function to also return action_loss2 and distribution_entropy_2

commented out code for using KFAC optimizer