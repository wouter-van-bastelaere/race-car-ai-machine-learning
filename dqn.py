#from fcntl import F_GETFD
from lib2to3.pgen2.pgen import DFAState
import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import deque

from car import Car

auto1 = Car()
repr(auto1)

class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        # De 8 inputs zijn x, y, rot, momentum, ang_momentum, obs[0], obs[1], obs[2]
        # De 4 outputs zijn telkens 0 of 1, afhankelijk of de pijlen 'Boven', 'Rechts', 'Onder', 'Boven'
        self.fc1 = nn.Linear(8, 30)
        self.fc2 = nn.Linear(30, 50)
        self.fc3 = nn.Linear(50, 4)
    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        return x

"""
print('hey')
dqn = DQN()
tens = torch.tensor([[1, 2, 3, 4, 5, 6, 7, 8]], dtype=torch.float32)
tens2 = torch.tensor([[1, 2, 3, 4, 5, 6, 7, 8]], dtype=torch.float32)
tens3 = torch.tensor([[1, 2, 3, 4, 5, 6, 7, 10]], dtype=torch.float32)
#torch.tensor(np.reshape(tens, [1, 8]), dtype = torch.float32)

print(tens)
y = dqn(tens)
y2 = dqn(tens2)
y3 = dqn(tens3)

print('hey')
for i in range(4):
    print(y[0][i])
print('he')
for i in range(4):
    print(y2[0][i])
print('hoi')
for i in range(4):
    print(y3[0][i])
"""

class DQN_solver:
    def __init__(self, gamma = 1, n_episodes = 100, eps_start = 1, eps_end = 0.1, eps_decay = 0.995, alpha = 0.01, alpha_end = 0, alpha_decay = 0.01, batch_size = 64, quiet = False):
        self.gamma = gamma
        self.n_episodes = n_episodes
        self.eps_start = eps_start
        self.eps_end = eps_end
        self.eps_decay = eps_decay
        self.memory = deque(maxlen=100000)
        self.alpha = alpha
        self.alpha_end = alpha_end
        self.alpha_decay = alpha_decay
        #Initialiseer model
        self.dqn = DQN()
        self.criterion = torch.nn.MSELoss()
        self.opt = torch.optim.Adam(self.dqn.parameters(), lr=0.01)
        self.batch_size = batch_size
        self.quiet = quiet
    def get_epsilon(self, t):
        return self.eps_end + (self.eps_start-self.eps_end)*np.exp(-t/self.eps_decay)

    def get_alpha(self, t):
        return self.alpha_end + (self.eps_alpha-self.eps_alpha)*np.exp(-t/self.eps_alpha)    

    def preprocess_state(self, state):
        return torch.tensor(np.reshape(state, [1, 8]), dtype = torch.float32)
    
    def choose_action(self, state, epsilon):
        epsilon = 1
        if np.random.random() < epsilon:
            print('random')
            action = (random.choice([True, False]), random.choice([True, False]))
            print(action)
            return action
        else:
            print('niet random')
            with torch.no_grad():
                return torch.argmax(self.dqn(state)).numpy()
    
    def remember(self, state, action, reward, next_state, done):
        reward = torch.tensor(reward)
        self.memory.append((state, action, reward, next_state, done))
    
    def replay(self, batch_size):
        #Nog niet veranderd
        y_batch, y_target_batch = [], []
        minibatch = random.sample(self.memory, min(len(self.memory), batch_size))
        for state, action, reward, next_state, done in minibatch:
            y = self.dqn(state)
            y_target = y.clone().detach()
            with torch.no_grad():
                y_target[0][action] = reward if done else reward + self.gamma * torch.max(self.dqn(next_state)[0])
            y_batch.append(y[0])
            y_target_batch.append(y_target[0])
        
        y_batch = torch.cat(y_batch)
        y_target_batch = torch.cat(y_target_batch)
        
        self.opt.zero_grad()
        loss = self.criterion(y_batch, y_target_batch)
        loss.backward()
        self.opt.step()        
        
        # if self.epsilon > self.epsilon_min:
        #     self.epsilon *= self.epsilon_decay

    def run(self):
        scores = deque(maxlen=100)
    
        for e in range(self.n_episodes):
            print(auto1)
            state = self.preprocess_state(auto1.State())
            print(f"state is {state}")
            done = False
            i = 0
            while not done:
                if e%100 == 0 and not self.quiet:
                    pass #render
                action = self.choose_action(state, self.get_epsilon(e))
                print(f"action is {action}")
                #next_state, reward, done, _ = _ #self.env.step(action)
                next_state, reward, done = auto1.Next_state(action), auto1.Reward(), auto1.Done()
                next_state = self.preprocess_state(next_state)
                self.remember(state, action, reward, next_state, done)
                state = next_state
                i += 1
            scores.append(i)
        mean_score = np.mean(scores)

agent = DQN_solver()
agent.run()


