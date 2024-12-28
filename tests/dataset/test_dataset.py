from src.dataset.dataset import Dataset


def test_split_dataset():
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


def test_binarize_labels():
    dataset = Dataset(
        [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
        ["A", "C", "B", "B"]
    )
    expected = Dataset(
        [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
        ["A", "other", "other", "other"]
    )
    assert dataset.binarize_labels("A") == expected


def test_unique_labels():
    dataset = Dataset(
        [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
        ["A", "C", "B", "B"]
    )
    assert dataset.unique_labels() == {"A", "C", "B"}


def test_subset_with_labels():
    dataset = Dataset(
        [("1", "2"), ("5", "1"), ("6", "3"), ("2", "3"), ("1", "2")],
        ["A", "C", "B", "D", "B"]
    )
    expected = Dataset(
        [("5", "1"), ("6", "3"), ("1", "2")],
        ["C", "B", "B"]
    )
    assert dataset.subset_with_labels({"C", "B"}) == expected

def test_shuffle():
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