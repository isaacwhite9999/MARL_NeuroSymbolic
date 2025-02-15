# app/agent.py

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class DQN(nn.Module):
    def __init__(self, input_dim=4, output_dim=5):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, output_dim)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

class DQNAgent:
    def __init__(self, learning_rate=0.001, discount_factor=0.99):
        self.model = DQN()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()
        self.discount_factor = discount_factor
    
    def select_action(self, state, epsilon=0.1):
        """
        Select an action using an epsilon-greedy policy.
        
        Args:
            state (np.array): The agent's state as a 4-dimensional vector.
            epsilon (float): Exploration rate.
        
        Returns:
            int: Chosen action index.
        """
        if np.random.rand() < epsilon:
            return np.random.randint(5)
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.model(state_tensor)
        return int(torch.argmax(q_values).item())
    
    def train_step(self, state, action, reward, next_state, done):
        """
        Perform a training step using the TD error.
        """
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0)
        q_values = self.model(state_tensor)
        target = q_values.clone().detach()
        with torch.no_grad():
            next_q_values = self.model(next_state_tensor)
        target_val = reward + (0 if done else self.discount_factor * torch.max(next_q_values).item())
        target[0, action] = target_val
        loss = self.criterion(q_values, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()
