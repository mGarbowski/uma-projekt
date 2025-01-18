from pytest import raises, fixture

from src.dataset.dataset import Dataset


@fixture
def kcv_dataset():
    return Dataset([
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"),
        ("10", "10")],
        ["A", "A", "A", "A", "B", "B", "B", "B", "C", "C"]
    )


class TestDataset:
    def test_split_dataset(self):
        dataset = Dataset(
            [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
            ["A", "A", "B", "B"]
        )

        expected_1 = Dataset(
            [("1", "2"), ("1", "2")],
            ["A", "B"]
        )

        expected_5 = Dataset(
            [("5", "1")],
            ["A"]
        )

        expected_6 = Dataset(
            [("6", "3")],
            ["B"]
        )

        after_split = dataset.split_by_attribute(attribute_idx=0)
        assert len(after_split) == 3
        assert expected_1 in after_split
        assert expected_5 in after_split
        assert expected_6 in after_split

    def test_binarize_labels(self):
        dataset = Dataset(
            [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
            ["A", "C", "B", "B"]
        )
        expected = Dataset(
            [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
            ["A", "other", "other", "other"]
        )
        assert dataset.binarize_labels("A") == expected

    def test_unique_labels(self):
        dataset = Dataset(
            [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
            ["A", "C", "B", "B"]
        )
        assert dataset.unique_labels() == {"A", "C", "B"}

    def test_subset_with_labels(self):
        dataset = Dataset(
            [("1", "2"), ("5", "1"), ("6", "3"), ("2", "3"), ("1", "2")],
            ["A", "C", "B", "D", "B"]
        )
        expected = Dataset(
            [("5", "1"), ("6", "3"), ("1", "2")],
            ["C", "B", "B"]
        )
        assert dataset.subset_with_labels({"C", "B"}) == expected

    def test_shuffle(self):
        dataset = Dataset(
            [("1", "2"), ("3", "4"), ("5", "6"), ("7", "8")],
            ["A", "B", "C", "D"]
        )
        dataset.shuffle()
        assert dataset.size() == 4
        assert dataset.attributes != [("1", "2"), ("3", "4"), ("5", "6"), ("7", "8")]
        assert dataset.labels != ["A", "B", "C", "D"]
        assert set(dataset.attributes) == {("1", "2"), ("3", "4"), ("5", "6"), ("7", "8")}
        assert set(dataset.labels) == {"A", "B", "C", "D"}
        assert dataset.attributes.index(("1", "2")) == dataset.labels.index("A")
        assert dataset.attributes.index(("3", "4")) == dataset.labels.index("B")
        assert dataset.attributes.index(("5", "6")) == dataset.labels.index("C")
        assert dataset.attributes.index(("7", "8")) == dataset.labels.index("D")

    def test_kcv_split(self, kcv_dataset):
        train_set, test_set = kcv_dataset.kcv_split(3, 0)
        assert train_set == Dataset([("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10")],
                                    ["B", "B", "B", "B", "C", "C"])
        assert test_set == Dataset([("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")], ["A", "A", "A", "A"])

        train_set, test_set = kcv_dataset.kcv_split(3, 1)
        assert train_set == Dataset(
            [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("8", "8"), ("9", "9"), ("10", "10")],
            ["A", "A", "A", "A", "B", "C", "C"])
        assert test_set == Dataset([("5", "5"), ("6", "6"), ("7", "7")], ["B", "B", "B"])

        train_set, test_set = kcv_dataset.kcv_split(3, 2)
        assert train_set == Dataset(
            [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7")],
            ["A", "A", "A", "A", "B", "B", "B"])
        assert test_set == Dataset([("8", "8"), ("9", "9"), ("10", "10")], ["B", "C", "C"])

    def test_kcv_split_invalid_k(self, kcv_dataset):
        with raises(ValueError):
            kcv_dataset.kcv_split(0, 0)
        with raises(ValueError):
            kcv_dataset.kcv_split(-1, 0)
        with raises(ValueError):
            kcv_dataset.kcv_split(1, 0)
        with raises(ValueError):
            kcv_dataset.kcv_split(11, 0)

    def test_kcv_split_invalid_i(self, kcv_dataset):
        with raises(ValueError):
            kcv_dataset.kcv_split(3, -1)
        with raises(ValueError):
            kcv_dataset.kcv_split(3, 3)

    def test_attributes_and_labels_must_have_equal_length(self):
        with raises(ValueError):
            Dataset([("1", "2"), ("5", "1"), ("6", "3")], ["A", "C", "B", "B"])

    def test_train_test_split_invalid_ratio(self):
        dataset = Dataset(
            [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
            ["A", "C", "B", "B"]
        )
        with raises(ValueError):
            dataset.train_test_split(-1)
        with raises(ValueError):
            dataset.train_test_split(2)
        with raises(ValueError):
            dataset.train_test_split(1.5)

    def test_train_test_split(self):
        dataset = Dataset(
            [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
            ["A", "C", "B", "B"]
        )

        train_set, test_set = dataset.train_test_split(0.45)
        assert len(train_set.labels) == len(train_set.attributes) == 1
        assert len(test_set.labels) == len(test_set.attributes) == 3

        train_set, test_set = dataset.train_test_split(0.5)
        assert len(train_set.labels) == len(train_set.attributes) == 2
        assert len(test_set.labels) == len(test_set.attributes) == 2

        train_set, test_set = dataset.train_test_split(0.74)
        assert len(train_set.labels) == len(train_set.attributes) == 2
        assert len(test_set.labels) == len(test_set.attributes) == 2

        train_set, test_set = dataset.train_test_split(0.76)
        assert len(train_set.labels) == len(train_set.attributes) == 3
        assert len(test_set.labels) == len(test_set.attributes) == 1
