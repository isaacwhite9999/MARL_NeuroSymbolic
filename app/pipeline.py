# app/pipeline.py

import argparse
from app.trainer import train_agents
from app.symbolic import explain_action
from app.env import MultiAgentEnv

def run_pipeline(num_episodes, epsilon):
    # Train agents
    agents = train_agents(num_episodes=num_episodes, epsilon=epsilon)
    
    # Evaluate agents in one episode and print actions with explanations
    env = MultiAgentEnv()
    state_dict = env.reset()
    actions = []
    explanations = []
    for i in range(env.num_agents):
        agent_pos = state_dict["agents"][i]
        goal = state_dict["goal"]
        state = [agent_pos[0], agent_pos[1], goal[0], goal[1]]
        action = agents[i].select_action(state, epsilon=0.0)  # Greedy selection during evaluation
        actions.append(action)
        explanation = explain_action(state, action)
        explanations.append(explanation)
    
    print("Evaluation:")
    for i in range(env.num_agents):
        print(f"Agent {i}: Action: {actions[i]}, Explanation: {explanations[i]}")

def main():
    parser = argparse.ArgumentParser(description="MARL with Neuro-Symbolic Reasoning Pipeline")
    parser.add_argument("--episodes", type=int, default=1000, help="Number of training episodes")
    parser.add_argument("--epsilon", type=float, default=0.1, help="Exploration rate")
    args = parser.parse_args()
    
    run_pipeline(args.episodes, args.epsilon)

if __name__ == "__main__":
    main()
