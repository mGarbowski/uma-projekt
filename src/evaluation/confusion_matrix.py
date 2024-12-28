from typing import Self


class ConfusionMatrix:
    _matrix: dict[str, dict[str, int]] = {}

    def __init__(self, matrix: dict[str, dict[str, int]] = None):
        if matrix is None:
            self._matrix = {}
            return

        self._matrix = matrix

    @classmethod
    def from_labels(cls, actual_labels: list[str], predicted_labels: list[str]) -> Self:
        if len(actual_labels) != len(predicted_labels):
            raise ValueError("actual_labels and predicted_labels must have equal length")

        matrix = {}
        all_labels = set(actual_labels) | set(predicted_labels)
        for label in all_labels:
            matrix[label] = {l: 0 for l in all_labels}

        for actual, predicted in zip(actual_labels, predicted_labels):
            matrix[actual][predicted] += 1

        return cls(matrix)

    def __repr__(self):
        return str(self._matrix)

    @property
    def matrix(self) -> dict[str, dict[str, int]]:
        return self._matrix
