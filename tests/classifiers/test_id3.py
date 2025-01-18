from math import log

from pytest import approx, raises, fixture

from src.classifiers.id3 import Dataset, entropy, most_common_element, build_decision_tree, best_split_idx, \
    information_gain, entropy_after_split, ID3Classifier, WeightedPrediction


class TestEntropy:
    def test_zero_entropy(self):
        dataset = Dataset(
            [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
            ["A", "A", "A", "A"]
        )

        assert entropy(dataset) == 0

    def test_entropy_with_one_element(self):
        dataset = Dataset(
            [("1", "2")],
            ["A"]
        )

        assert entropy(dataset) == 0

    def test_max_entropy(self):
        dataset = Dataset(
            [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
            ["A", "A", "B", "B"]
        )

        assert entropy(dataset) == 1

    def test_entropy_between_zero_and_max(self):
        dataset = Dataset(
            [("A", "1"), ("B", "1"), ("B", "2"), ("B", "2"), ("B", "3")],
            ["0", "1", "1", "0", "1"]
        )

        assert entropy(dataset) == approx(-2 / 5 * log(2 / 5, 2) - 3 / 5 * log(3 / 5, 2))


class TestEntropyAfterSplit:
    def test_split_by_attribute_0(self):
        dataset = Dataset(
            [("A", "1"), ("B", "1"), ("B", "2"), ("B", "2"), ("B", "3")],
            ["0", "1", "1", "0", "1"]
        )

        partition_a = Dataset([("A", "1")], ["0"])
        partition_b = Dataset([("B", "1"), ("B", "2"), ("B", "2"), ("B", "3")], ["1", "1", "0", "1"])
        expected = 1 / 5 * entropy(partition_a) + 4 / 5 * entropy(partition_b)
        assert entropy_after_split(dataset, 0) == approx(expected)


class TestMostCommonElement:
    def test_most_common_element(self):
        elements = [1, 6, 4, 2, 6, 1, 2, 2]
        element, weight = most_common_element(elements)
        assert element == 2
        assert weight == approx(3 / 8)


class TestInformationGain:
    def test_information_gain(self):
        dataset = Dataset(
            [("A", "1"), ("B", "1"), ("B", "2"), ("B", "2"), ("B", "3")],
            ["0", "1", "1", "0", "1"]
        )

        dataset_entropy = -2 / 5 * log(2 / 5, 2) - 3 / 5 * log(3 / 5, 2)
        partition_a_entropy = 0
        partition_b_entropy = -1 / 4 * log(1 / 4, 2) - 3 / 4 * log(3 / 4, 2)
        expected = dataset_entropy - 1 / 5 * partition_a_entropy - 4 / 5 * partition_b_entropy
        assert information_gain(dataset, 0) == approx(expected)


class TestBestSplitIdx:
    def test_best_split_idx(self):
        dataset = Dataset(
            [("A", "1"), ("B", "1"), ("B", "2"), ("B", "2"), ("B", "3")],
            ["0", "1", "1", "0", "1"]
        )

        assert information_gain(dataset, 0) > information_gain(dataset, 1)
        assert best_split_idx(dataset, set(range(2))) == 0


class TestBuildDecisionTree:

    def test_raises_error_if_dataset_is_empty(self):
        available_attribute_idxs = set()
        dataset = Dataset([], [])

        with raises(ValueError):
            build_decision_tree(dataset, available_attribute_idxs)

    def test_uniform_class(self):
        available_attribute_idxs = set(range(2))
        dataset = Dataset(
            [("A", "1"), ("B", "2"), ("C", "3")],
            ["0", "0", "0"]
        )

        tree = build_decision_tree(dataset, available_attribute_idxs)
        assert tree.is_leaf()
        assert tree.leaf_label == "0"
        assert tree.weight == 1

    def test_no_attributes(self):
        available_attribute_idxs = set()  # no attributes left to split on
        dataset = Dataset(
            [("A", "1"), ("B", "2"), ("C", "3")],
            ["0", "0", "1"]
        )

        tree = build_decision_tree(dataset, available_attribute_idxs)
        assert tree.is_leaf()
        assert tree.leaf_label == "0"
        assert tree.weight == approx(2 / 3)

    def test_build_tree_on_example_dataset(self):
        available_attribute_idxs = set(range(2))
        dataset = Dataset(
            [("A", "1"), ("B", "1"), ("B", "2"), ("B", "2"), ("B", "3")],
            ["0", "1", "1", "0", "1"]
        )

        tree_root = build_decision_tree(dataset, available_attribute_idxs.copy())

        # First split is by attribute 0
        assert best_split_idx(dataset, available_attribute_idxs.copy()) == 0
        assert not tree_root.is_leaf()
        assert tree_root.split_attribute_idx == 0
        assert len(tree_root.children) == 2
        assert "A" in tree_root.children
        assert "B" in tree_root.children
        assert tree_root.most_common_label == "1"

        # Left child is a leaf built for partitioned dataset with just the first row (A, 1, 0)
        node_a = tree_root.children["A"]
        assert node_a.is_leaf()
        assert node_a.leaf_label == "0"
        assert node_a.weight == 1

        # Right child is a subtree, only attribute 1 is left to split
        node_b = tree_root.children["B"]
        assert not node_b.is_leaf()
        assert node_b.split_attribute_idx == 1
        assert node_b.most_common_label == "1"
        assert node_b.weight == approx(3 / 4)  # 3x"1" and 1x"0"
        assert len(node_b.children) == 3
        assert "1" in node_b.children
        assert "2" in node_b.children
        assert "3" in node_b.children

        # Build for partition with row (B, 1, 1)
        node_b_1 = node_b.children["1"]
        assert node_b_1.is_leaf()
        assert node_b_1.leaf_label == "1"
        assert node_b_1.weight == 1

        # Build for partition with rows (B, 2, 1) and (B, 2, 0)
        node_b_2 = node_b.children["2"]
        assert node_b_2.is_leaf()
        assert node_b_2.leaf_label == "0" or node_b_2.leaf_label == "1"  # they have equal weight
        assert node_b_2.weight == approx(1 / 2)  # 1x"1" and 1x"0"

        # Build for partition with row (B, 3, 1)
        node_b_3 = node_b.children["3"]
        assert node_b_3.is_leaf()
        assert node_b_3.leaf_label == "1"
        assert node_b_3.weight == 1


@fixture()
def trained_model():
    dataset = Dataset(
        [("A", "1"), ("B", "1"), ("B", "2"), ("B", "2"), ("B", "3")],
        ["0", "1", "1", "0", "1"]
    )

    return ID3Classifier.train(dataset)


class TestID3Classifier:
    def test_name(self):
        assert ID3Classifier.name() == "ID3"

    def test_predict_with_attribute_value_not_present_in_train_set(self, trained_model):
        assert trained_model.predict_single_with_weight(("A", "4")) == WeightedPrediction("0", 1)
        assert trained_model._root.children["A"].most_common_label == "0"
        assert trained_model._root.children["A"].weight == 1

        assert trained_model.predict_single_with_weight(("C", "2")) == WeightedPrediction("1", 0.6)
        assert trained_model._root.most_common_label == "1"
        assert trained_model._root.weight == 0.6

    def test_predict_single(self, trained_model):
        assert trained_model.predict_single(("A", "1")) == "0"
        assert trained_model.predict_single(("A", "2")) == "0"
        assert trained_model.predict_single(("A", "3")) == "0"

        assert trained_model.predict_single(("B", "1")) == "1"
        assert trained_model.predict_single(("B", "2")) == "1"
        assert trained_model.predict_single(("B", "3")) == "1"

    def test_predict_single_with_weight(self, trained_model):
        assert trained_model.predict_single_with_weight(("A", "1")) == WeightedPrediction("0", 1)
        assert trained_model.predict_single_with_weight(("A", "2")) == WeightedPrediction("0", 1)
        assert trained_model.predict_single_with_weight(("A", "3")) == WeightedPrediction("0", 1)

        assert trained_model.predict_single_with_weight(("B", "1")) == WeightedPrediction("1", 1)
        assert trained_model.predict_single_with_weight(("B", "2")) == WeightedPrediction("1", 0.5)
        assert trained_model.predict_single_with_weight(("B", "3")) == WeightedPrediction("1", 1)

    def test_predict_with_weights(self, trained_model):
        predictions = trained_model.predict_with_weights([
            ("A", "1"), ("A", "2"), ("A", "3"),
            ("B", "1"), ("B", "2"), ("B", "3")
        ])

        assert predictions == [
            WeightedPrediction("0", 1),
            WeightedPrediction("0", 1),
            WeightedPrediction("0", 1),
            WeightedPrediction("1", 1),
            WeightedPrediction("1", 0.5),
            WeightedPrediction("1", 1)
        ]

    def test_predict(self, trained_model):
        predictions = trained_model.predict([
            ("A", "1"), ("A", "2"), ("A", "3"),
            ("B", "1"), ("B", "2"), ("B", "3")
        ])

        assert predictions == ["0", "0", "0", "1", "1", "1"]
