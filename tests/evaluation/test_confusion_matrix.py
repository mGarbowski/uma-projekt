from src.evaluation.confusion_matrix import ConfusionMatrix


def test_from_labels_3x3():
    predicted_labels = ["a", "b", "c", "a", "b", "c", "a", "b", "c"]
    actual_labels = ["a", "b", "a", "b", "b", "b", "c", "b", "c"]
    expected = {
        "a": {"a": 1, "b": 0, "c": 1},
        "b": {"a": 1, "b": 3, "c": 1},
        "c": {"a": 1, "b": 0, "c": 1}
    }

    confusion_matrix = ConfusionMatrix.from_labels(actual_labels, predicted_labels)
    assert confusion_matrix.matrix == expected
