import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import deque

class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        # De 8 inputs zijn x, y, rot, momentum, ang_momentum, obs[0], obs[1], obs[2]
        # De 2 outputs zijn kracht, torque
        self.fc1 = nn.Linear(8, 30)
        self.fc2 = nn.Linear(30, 50)
        self.fc3 = nn.Linear(50, 2)
def forward(self, x):
    x = self.fc1(x)
    x = F.relu(x)
    x = self.fc2(x)
    x = F.relu(x)
    x = self.fc3(x)
    return x

class DQN_solver:
    def __init__(self, gamma = 1, n_episodes = 100, eps_start = 1, eps_end = 0.1, eps_decay = 0):
        self.gamma = gamma
        self.n_episodes = n_episodes
        self.eps_start = eps_start
        self.eps_end = eps_end
        self.eps_decay = eps_decay
        self.memory = deque(maxlen=100000)
        #Initialiseer model
        self.dqn = DQN()
        self.criterion = torch.nn.MSELoss()
        self.opt = torch.optim.Adam(self.dqn.parameters(), lr=0.01)
    def get_epsilon(self, t):
        return eps_end + (eps_start-eps_end)*np.exp(-t/eps_decay)

    def preprocess_state(self, state):
        return torch.tensor(np.reshape(state, [1, 8]), dtype = torch.float32)
    
    def choose_action(self, state, epsilon):
        if np.random.random() < epsilon:
            pass #random
        else:
            with torch.no_grad():
                return torch.argmax(self.dqn(state)).numpy()
    
    def remember(self, state, actie, reward, next_state, done):
        reward = torch.tensor(reward)
        self.memory.append((state, actie, reward, next_state, done))
    
    def replay(self, batch_size):
        #Nog niet veranderd
        y_batch, y_target_batch = [], []
        minibatch = random.sample(self.memory, min(len(self.memory), batch_size))
        for state, actie, reward, next_state, done in minibatch:
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
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay




