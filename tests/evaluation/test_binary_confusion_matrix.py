from src.evaluation.binary_confusion_matrix import BinaryConfusionMatrix
from src.evaluation.confusion_matrix import ConfusionMatrix


def test_from_confusion_matrix():
    confusion_matrix = ConfusionMatrix({
        "a": {"a": 1, "b": 0, "c": 1},
        "b": {"a": 1, "b": 3, "c": 1},
        "c": {"a": 1, "b": 0, "c": 1}
    })

    assert BinaryConfusionMatrix.from_multiclass(confusion_matrix, "a") == BinaryConfusionMatrix(1, 4, 2, 1)
    assert BinaryConfusionMatrix.from_multiclass(confusion_matrix, "b") == BinaryConfusionMatrix(3, 2, 0, 2)
    assert BinaryConfusionMatrix.from_multiclass(confusion_matrix, "c") == BinaryConfusionMatrix(1, 4, 2, 1)