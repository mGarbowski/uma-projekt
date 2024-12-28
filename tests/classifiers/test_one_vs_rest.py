from unittest.mock import Mock

from src.classifiers.id3 import WeightedPrediction
from src.classifiers.one_vs_rest import OneVsRestClassifier


def given_tree_that_predicts(label: str, weight: float) -> Mock:
    tree = Mock()
    tree.predict_single_with_weight.return_value = WeightedPrediction(label, weight)
    return tree

def test_ovr_predicts_positive_class_with_highest_weight():
    tree_a = given_tree_that_predicts("A", 0.8)
    tree_b = given_tree_that_predicts("other", 0.7)
    tree_c = given_tree_that_predicts("C", 0.7)
    tree_d = given_tree_that_predicts("other", 0.9)
    ovr_model = OneVsRestClassifier({"A": tree_a, "B": tree_b, "C": tree_c, "D": tree_d})

    assert ovr_model.predict_single(("blah", "blah", "blah")) == "A"

def test_ovr_predicts_negative_class_with_lowest_weight_when_no_positive_prediction():
    tree_a = given_tree_that_predicts("other", 0.9)
    tree_b = given_tree_that_predicts("other", 0.7)
    tree_c = given_tree_that_predicts("other", 0.8)
    tree_d = given_tree_that_predicts("other", 0.5)
    ovr_model = OneVsRestClassifier({"A": tree_a, "B": tree_b, "C": tree_c, "D": tree_d})

    assert ovr_model.predict_single(("blah", "blah", "blah")) == "D"