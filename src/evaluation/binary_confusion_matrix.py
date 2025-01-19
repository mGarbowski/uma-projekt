"""Authors: Mikołaj Garbowski, Michał Pałasz"""

from dataclasses import dataclass
from typing import Self

from src.evaluation.confusion_matrix import ConfusionMatrix


@dataclass
class BinaryConfusionMatrix:
    true_positives: int = 0
    true_negatives: int = 0
    false_positives: int = 0
    false_negatives: int = 0

    def __str__(self):
        return f"TP: {self.true_positives}, TN: {self.true_negatives}, FP: {self.false_positives}, FN: {self.false_negatives}"

    def __eq__(self, other):
        return self.true_positives == other.true_positives and self.true_negatives == other.true_negatives and \
            self.false_positives == other.false_positives and self.false_negatives == other.false_negatives

    @classmethod
    def from_multiclass(cls, matrix: ConfusionMatrix, positive_label: str) -> Self:
        negative_labels = matrix.labels()
        negative_labels.remove(positive_label)

        tp = matrix.matrix[positive_label][positive_label]
        fp = sum(matrix.matrix[neg_actual][positive_label] for neg_actual in negative_labels)
        fn = sum(matrix.matrix[positive_label][neg_predicted] for neg_predicted in negative_labels)
        tn = sum(matrix.matrix[negative][negative] for negative in negative_labels)

        return cls(tp, tn, fp, fn)

    @classmethod
    def sum(cls, matrices: list[Self]) -> Self:
        tp = sum(matrix.true_positives for matrix in matrices)
        tn = sum(matrix.true_negatives for matrix in matrices)
        fp = sum(matrix.false_positives for matrix in matrices)
        fn = sum(matrix.false_negatives for matrix in matrices)

        return cls(tp, tn, fp, fn)

    def accuracy(self) -> float:
        try:
            return (self.true_positives + self.true_negatives) / (self.true_positives + self.true_negatives +
                                                                  self.false_positives + self.false_negatives)
        except ZeroDivisionError:
            return 0.0

    def recall(self) -> float:
        try:
            return self.true_positives / (self.true_positives + self.false_negatives)
        except ZeroDivisionError:
            return 0.0

    def precision(self) -> float:
        try:
            return self.true_positives / (self.true_positives + self.false_positives)
        except ZeroDivisionError:
            return 0.0

    def f_measure(self) -> float:
        precision = self.precision()
        recall = self.recall()
        try:
            return 2 * precision * recall / (precision + recall)
        except ZeroDivisionError:
            return 0.0

    def specificity(self) -> float:
        try:
            return self.true_negatives / (self.true_negatives + self.false_positives)
        except ZeroDivisionError:
            return 0.0

    def tp_rate(self) -> float:
        return self.recall()

    def fp_rate(self) -> float:
        try:
            return self.false_positives / (self.false_positives + self.true_negatives)
        except ZeroDivisionError:
            return 0.0
