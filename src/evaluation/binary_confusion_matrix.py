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
        negative_labels = list(matrix.matrix.keys())
        negative_labels.remove(positive_label)

        tp = matrix.matrix[positive_label][positive_label]
        fp = sum(matrix.matrix[neg_actual][positive_label] for neg_actual in negative_labels)
        fn = sum(matrix.matrix[positive_label][neg_predicted] for neg_predicted in negative_labels)
        tn = sum(matrix.matrix[negative][negative] for negative in negative_labels)

        return cls(tp, tn, fp, fn)
