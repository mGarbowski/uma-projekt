from src.classifiers.id3 import ID3Classifier
from src.classifiers.one_vs_one import get_pairs, OneVsOneClassifier
from src.dataset.dataset import Dataset
from tests.utils import given_tree_that_predicts


def test_get_pairs():
    labels = {"A", "B", "C"}
    pairs = get_pairs(labels)
    assert len(pairs) == 3
    assert ("A", "B") in pairs or ("B", "A") in pairs
    assert ("A", "C") in pairs or ("C", "A") in pairs
    assert ("B", "C") in pairs or ("C", "B") in pairs


class TestOneVsOneClassifier:
    def test_name(self):
        assert OneVsOneClassifier.name() == "One-vs-One"

    def test_predicts_label_with_highest_weighted_vote(self):
        tree_ab = given_tree_that_predicts("A", 0.99)
        tree_bc = given_tree_that_predicts("B", 0.8)
        tree_ac = given_tree_that_predicts("C", 0.07)
        ovo_model = OneVsOneClassifier(
            {("A", "B"): tree_ab, ("B", "C"): tree_bc, ("A", "C"): tree_ac},
            ("A", "B", "C")
        )

        assert ovo_model.predict_single(("blah", "blah", "blah")) == "A"

    def test_creates_trees_for_each_pair_of_classes(self):
        dataset = Dataset(
            [("A", "1"), ("B", "1"), ("B", "2"), ("B", "2"), ("B", "3")],
            ["0", "1", "2", "3", "1"]
        )
        ovo_model = OneVsOneClassifier.train(dataset)

        assert len(ovo_model._trees) == 6
        assert len(get_pairs(dataset.unique_labels())) == 6
        assert all(isinstance(tree, ID3Classifier) for tree in ovo_model._trees.values())
