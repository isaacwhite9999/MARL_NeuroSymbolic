# app/trainer.py

import numpy as np
from app.env import MultiAgentEnv
from app.agent import DQNAgent

def train_agents(num_episodes=1000, max_steps=50, epsilon=0.1):
    env = MultiAgentEnv()
    num_agents = env.num_agents
    agents = [DQNAgent() for _ in range(num_agents)]
    
    for episode in range(num_episodes):
        state_dict = env.reset()
        done = False
        total_reward = [0 for _ in range(num_agents)]
        
        for step in range(max_steps):
            states = []
            actions = []
            for i in range(num_agents):
                agent_pos = state_dict["agents"][i]
                goal = state_dict["goal"]
                state = [agent_pos[0], agent_pos[1], goal[0], goal[1]]
                states.append(state)
                action = agents[i].select_action(state, epsilon)
                actions.append(action)
            next_state_dict, rewards, done, _ = env.step(actions)
            
            for i in range(num_agents):
                agent_pos = state_dict["agents"][i]
                goal = state_dict["goal"]
                state = [agent_pos[0], agent_pos[1], goal[0], goal[1]]
                next_agent_pos = next_state_dict["agents"][i]
                next_state = [next_agent_pos[0], next_agent_pos[1], goal[0], goal[1]]
                loss = agents[i].train_step(state, actions[i], rewards[i], next_state, done)
                total_reward[i] += rewards[i]
            
            state_dict = next_state_dict
            if done:
                break
        
        if episode % 100 == 0:
            print(f"Episode {episode}: Total rewards: {total_reward}")
    return agents
