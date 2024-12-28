from src.classifiers.one_vs_one import get_pairs, OneVsOneClassifier
from tests.utils import given_tree_that_predicts


def test_get_pairs():
    labels = {"A", "B", "C"}
    pairs = get_pairs(labels)
    assert len(pairs) == 3
    assert ("A", "B") in pairs or ("B", "A") in pairs
    assert ("A", "C") in pairs or ("C", "A") in pairs
    assert ("B", "C") in pairs or ("C", "B") in pairs


def test_ovo_predicts_label_with_highest_weighted_vote():
    tree_ab = given_tree_that_predicts("A", 0.99)
    tree_bc = given_tree_that_predicts("B", 0.8)
    tree_ac = given_tree_that_predicts("C", 0.07)
    ovo_model = OneVsOneClassifier(
        {("A", "B"): tree_ab, ("B", "C"): tree_bc, ("A", "C"): tree_ac},
        ("A", "B", "C")
    )

    assert ovo_model.predict_single(("blah", "blah", "blah")) == "A"
