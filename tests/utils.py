from unittest.mock import Mock

from src.classifiers.id3 import WeightedPrediction


def given_tree_that_predicts(label: str, weight: float) -> Mock:
    tree = Mock()
    tree.predict_single_with_weight.return_value = WeightedPrediction(label, weight)
    return tree