# app/env.py

import numpy as np

class MultiAgentEnv:
    def __init__(self, grid_size=5, num_agents=2):
        self.grid_size = grid_size
        self.num_agents = num_agents
        self.agent_positions = None
        self.goal = (grid_size - 1, grid_size - 1)
    
    def reset(self):
        # Reset: All agents start at (0,0)
        self.agent_positions = [(0, 0) for _ in range(self.num_agents)]
        return self._get_state()
    
    def _get_state(self):
        # Return the current state as a dict with agent positions and goal
        return {"agents": self.agent_positions, "goal": self.goal}
    
    def step(self, actions):
        """
        Execute actions for each agent.
        
        Actions: 
          0: up, 1: right, 2: down, 3: left, 4: stay
        """
        rewards = [0 for _ in range(self.num_agents)]
        done = False
        
        for i, action in enumerate(actions):
            x, y = self.agent_positions[i]
            if action == 0:  # up
                x = max(0, x - 1)
            elif action == 1:  # right
                y = min(self.grid_size - 1, y + 1)
            elif action == 2:  # down
                x = min(self.grid_size - 1, x + 1)
            elif action == 3:  # left
                y = max(0, y - 1)
            elif action == 4:  # stay
                pass
            self.agent_positions[i] = (x, y)
        
        # Cooperative reward: if all agents reach the goal, they get a bonus reward.
        if all(pos == self.goal for pos in self.agent_positions):
            rewards = [10 for _ in range(self.num_agents)]
            done = True
        else:
            rewards = [-0.1 for _ in range(self.num_agents)]
        return self._get_state(), rewards, done, {}
