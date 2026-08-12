"""
Pulse Multi-Objective Decision Optimizer.

Selects the most appropriate maintenance action by balancingasset health, priority, urgency, and replacement requirements.
"""

from src.config.constants import HealthStatus, Recommendation


def calculate_best_action(health_status, health_score, priority_weight):
    """
    Calculate scores for available maintenance actions and select the action with the highest score.

    """
    repair_score = 0.0

    if health_status == HealthStatus.WARNING:
        repair_score += 40.0
    elif health_status == HealthStatus.CRITICAL:
        repair_score += 70.0

    repair_score += priority_weight * 3.0


    delay_score = float(health_score * 0.6)


    replace_score = 0.0
    if (health_status == HealthStatus.CRITICAL and health_score < 30):
        replace_score += 95.0
    replace_score += priority_weight * 2.0
    options = {
        Recommendation.REPAIR: round(repair_score, 1),
        Recommendation.DELAY: round(delay_score, 1),
        Recommendation.REPLACE: round(replace_score, 1),
    }

    best_action = max(options, key=options.get)

    return best_action, options