from src.classifiers.one_vs_rest import OneVsRestClassifier
from tests.utils import given_tree_that_predicts


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
