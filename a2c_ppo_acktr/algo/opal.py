import torch
import torch.nn as nn
import torch.optim as optim

#from a2c_ppo_acktr.algo.kfac import KFACOptimizer


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
        

        # if acktr:
        #     self.optimizer = KFACOptimizer(actor_critic)
        # else:
        #     self.optimizer = optim.RMSprop(
        #         actor_critic.parameters(), lr, eps=eps, alpha=alpha)

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
        
        # values2, action_log_probs2, dist_entropy2, _ = self.actor_critic.evaluate_actions2(
        #     rollouts.obs[:-1].view(-1, *obs_shape),
        #     rollouts.recurrent_hidden_states[0].view(
        #         -1, self.actor_critic.recurrent_hidden_state_size),
        #     rollouts.masks[:-1].view(-1, 1),
        #     rollouts.actions2.view(-1, action_shape))
    
    
        #values2 = values2.view(num_steps, num_processes, 1)
        action_log_probs2 = action_log_probs2.view(num_steps, num_processes, 1)

        # advantages2 = rollouts.returns[:-1] - values2
        # value_loss2 = advantages2.pow(2).mean()

        action_loss2 = -(advantages.detach() * action_log_probs2).mean()
        
        # print("log prob",action_log_probs2==action_log_probs)
        # print("entropy",dist_entropy==dist_entropy2)
        
        

        # if self.acktr and self.optimizer.steps % self.optimizer.Ts == 0:
        #     # Compute fisher, see Martens 2014
        #     self.actor_critic.zero_grad()
        #     pg_fisher_loss = -action_log_probs.mean()

        #     value_noise = torch.randn(values.size())
        #     if values.is_cuda:
        #         value_noise = value_noise.cuda()

        #     sample_values = values + value_noise
        #     vf_fisher_loss = -(values - sample_values.detach()).pow(2).mean()

        #     fisher_loss = pg_fisher_loss + vf_fisher_loss
        #     self.optimizer.acc_stats = True
        #     fisher_loss.backward(retain_graph=True)
        #     self.optimizer.acc_stats = False

        self.optimizer.zero_grad()
        # (value_loss * self.value_loss_coef + action_loss -
        #  dist_entropy * self.entropy_coef).backward()
        (value_loss * self.value_loss_coef + action_loss + action_loss2 -
         dist_entropy * self.entropy_coef - dist_entropy2 * self.entropy_coef).backward()

        if self.acktr == False:
            nn.utils.clip_grad_norm_(self.actor_critic.parameters(),
                                     self.max_grad_norm)

        self.optimizer.step()
        #the return goes to the main.py file where these values are just used to print while training

        return value_loss.item(), action_loss.item(), dist_entropy.item(), action_loss2.item(), dist_entropy2.item()
