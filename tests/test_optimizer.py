from src.config.constants import HealthStatus, Recommendation
from src.optimizer import calculate_best_action


def test_optimizer_decision_matrix():
    """
    Test whether the optimizer selects appropriate actions for different asset health conditions.

    """

    action_1, scores_1 = calculate_best_action(HealthStatus.CRITICAL, 15.0, 5.0)
    assert action_1 == Recommendation.REPLACE

    
    action_2, scores_2 = calculate_best_action(HealthStatus.HEALTHY, 95.0, 1.0)
    assert action_2 == Recommendation.DELAY