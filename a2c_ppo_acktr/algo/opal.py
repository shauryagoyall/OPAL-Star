import torch
import torch.nn as nn
import torch.optim as optim

class OPAL():
    def __init__(self,
                 actor_critic,
                 value_loss_coef,
                 entropy_coef,
                 lr=None,
                 eps=None,
                 alpha=None,
                 max_grad_norm=None,
                 acktr=False):

        self.actor_critic = actor_critic
        self.acktr = acktr

        self.value_loss_coef = value_loss_coef
        self.entropy_coef = entropy_coef

        self.max_grad_norm = max_grad_norm
        
        self.optimizer = optim.RMSprop(
            actor_critic.parameters(), lr, eps=eps, alpha=alpha)
        

    def update(self, rollouts):
        obs_shape = rollouts.obs.size()[2:]
        action_shape = rollouts.actions.size()[-1]
        num_steps, num_processes, _ = rollouts.rewards.size()

        values, action_log_probs, action_log_probs2, dist_entropy, dist_entropy2, _ = self.actor_critic.evaluate_actions(
            rollouts.obs[:-1].view(-1, *obs_shape),
            rollouts.recurrent_hidden_states[0].view(
                -1, self.actor_critic.recurrent_hidden_state_size),
            rollouts.masks[:-1].view(-1, 1),
            rollouts.actions.view(-1, action_shape))
  
        values = values.view(num_steps, num_processes, 1)
        action_log_probs = action_log_probs.view(num_steps, num_processes, 1)

        advantages = rollouts.returns[:-1] - values
        value_loss = advantages.pow(2).mean()

        action_loss = -(advantages.detach() * action_log_probs).mean()
        
        ## For the 2nd actor
        action_log_probs2 = action_log_probs2.view(num_steps, num_processes, 1)
        action_loss2 = -(advantages.detach() * action_log_probs2).mean()
     
        self.optimizer.zero_grad()
        (value_loss * self.value_loss_coef + action_loss + action_loss2 -
         dist_entropy * self.entropy_coef - dist_entropy2 * self.entropy_coef).backward() # modified loss to include contribution from 2nd actor

        if self.acktr == False:
            nn.utils.clip_grad_norm_(self.actor_critic.parameters(),
                                     self.max_grad_norm)

        self.optimizer.step()
        
        #the return goes to the main.py file where these values are just used to print while training
        return value_loss.item(), action_loss.item(), dist_entropy.item(), action_loss2.item(), dist_entropy2.item()
