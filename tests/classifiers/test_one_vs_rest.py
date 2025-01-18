from src.classifiers.id3 import ID3Classifier
from src.classifiers.one_vs_rest import OneVsRestClassifier
from src.dataset.dataset import Dataset
from tests.utils import given_tree_that_predicts


class TestOneVsRestClassifier:
    def test_name(self):
        assert OneVsRestClassifier.name() == "One-vs-Rest"

    def test_creates_trees_for_each_class(self):
        dataset = Dataset(
            [("A", "1"), ("B", "1"), ("B", "2"), ("B", "2"), ("B", "3")],
            ["0", "1", "2", "3", "1"]
        )
        ovr_model = OneVsRestClassifier.train(dataset)

        assert len(ovr_model._trees) == 4
        assert len(dataset.unique_labels()) == 4
        assert all(isinstance(tree, ID3Classifier) for tree in ovr_model._trees.values())

    def test_predicts_positive_class_with_highest_weight(self):
        tree_a = given_tree_that_predicts("A", 0.8)
        tree_b = given_tree_that_predicts("other", 0.7)
        tree_c = given_tree_that_predicts("C", 0.7)
        tree_d = given_tree_that_predicts("other", 0.9)
        ovr_model = OneVsRestClassifier({"A": tree_a, "B": tree_b, "C": tree_c, "D": tree_d})

        assert ovr_model.predict_single(("blah", "blah", "blah")) == "A"

    def test_predicts_negative_class_with_lowest_weight_when_no_positive_prediction(self):
        tree_a = given_tree_that_predicts("other", 0.9)
        tree_b = given_tree_that_predicts("other", 0.7)
        tree_c = given_tree_that_predicts("other", 0.8)
        tree_d = given_tree_that_predicts("other", 0.5)
        ovr_model = OneVsRestClassifier({"A": tree_a, "B": tree_b, "C": tree_c, "D": tree_d})

        assert ovr_model.predict_single(("blah", "blah", "blah")) == "D"
