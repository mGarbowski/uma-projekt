from dataclasses import dataclass
from statistics import mean
from typing import Self

from src.evaluation.binary_confusion_matrix import BinaryConfusionMatrix
from src.evaluation.confusion_matrix import ConfusionMatrix


@dataclass
class Evaluation:
    accuracy: float
    recall: float
    precision: float
    f_measure: float
    specificity: float
    tp_rate: float
    fp_rate: float

    @classmethod
    def from_binary_confusion_matrix(cls, binary_confusion_matrix: BinaryConfusionMatrix) -> Self:
        return cls(
            binary_confusion_matrix.accuracy(),
            binary_confusion_matrix.recall(),
            binary_confusion_matrix.precision(),
            binary_confusion_matrix.f_measure(),
            binary_confusion_matrix.specificity(),
            binary_confusion_matrix.tp_rate(),
            binary_confusion_matrix.fp_rate()
        )

    @classmethod
    def micro_average(cls, confusion_matrix: ConfusionMatrix) -> Self:
        labels = confusion_matrix.labels()
        binary_matrices = [BinaryConfusionMatrix.from_multiclass(confusion_matrix, label) for label in labels]
        aggregate_matrix = BinaryConfusionMatrix.sum(binary_matrices)
        return cls.from_binary_confusion_matrix(aggregate_matrix)

    @classmethod
    def macro_average(cls, confusion_matrix: ConfusionMatrix) -> Self:
        labels = confusion_matrix.labels()
        evaluations = [
            Evaluation.from_binary_confusion_matrix(
                BinaryConfusionMatrix.from_multiclass(confusion_matrix, label)
            )
            for label in labels
        ]

        return cls(
            accuracy=mean(e.accuracy for e in evaluations),
            recall=mean(e.recall for e in evaluations),
            precision=mean(e.precision for e in evaluations),
            f_measure=mean(e.f_measure for e in evaluations),
            specificity=mean(e.specificity for e in evaluations),
            tp_rate=mean(e.tp_rate for e in evaluations),
            fp_rate=mean(e.fp_rate for e in evaluations)
        )
