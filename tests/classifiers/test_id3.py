from pytest import approx

from src.classifiers.id3 import Dataset, entropy, most_common_element


def test_zero_entropy():
    dataset = Dataset(
        [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
        ["A", "A", "A", "A"]
    )

    assert entropy(dataset) == 0


def test_max_entropy():
    dataset = Dataset(
        [("1", "2"), ("5", "1"), ("6", "3"), ("1", "2")],
        ["A", "A", "B", "B"]
    )

    assert entropy(dataset) == 1


def test_most_common_element():
    elements = [1, 6, 4, 2, 6, 1, 2, 2]
    element, weight = most_common_element(elements)
    assert element == 2
    assert weight == approx(3 / 8)
