# app/symbolic.py

def explain_action(state, action):
    """
    Provide a symbolic explanation for an agent's action based on its state.
    
    Args:
        state (list): [agent_x, agent_y, goal_x, goal_y]
        action (int): Action taken (0: up, 1: right, 2: down, 3: left, 4: stay)
    
    Returns:
        str: Human-readable explanation of the action.
    """
    agent_x, agent_y, goal_x, goal_y = state
    explanation = ""
    if action == 0:
        explanation = "Moved up"
        if goal_x < agent_x:
            explanation += " because the goal is above."
        else:
            explanation += ", though the goal is not above."
    elif action == 1:
        explanation = "Moved right"
        if goal_y > agent_y:
            explanation += " because the goal is to the right."
        else:
            explanation += ", though the goal is not to the right."
    elif action == 2:
        explanation = "Moved down"
        if goal_x > agent_x:
            explanation += " because the goal is below."
        else:
            explanation += ", though the goal is not below."
    elif action == 3:
        explanation = "Moved left"
        if goal_y < agent_y:
            explanation += " because the goal is to the left."
        else:
            explanation += ", though the goal is not to the left."
    elif action == 4:
        explanation = "Stayed in place."
    return explanation
