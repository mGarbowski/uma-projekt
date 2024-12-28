from src.classifiers.one_vs_one import get_pairs


def test_get_pairs():
    labels = {"A", "B", "C"}
    pairs = get_pairs(labels)
    assert len(pairs) == 3
    assert ("A", "B") in pairs
    assert ("A", "C") in pairs
    assert ("B", "C") in pairs