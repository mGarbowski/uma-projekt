"""Authors: Mikołaj Garbowski, Michał Pałasz"""

from dataclasses import dataclass
from statistics import mean, stdev
from typing import Self

from src.evaluation.evaluation import Evaluation


@dataclass
class AggregateEvaluation:
    accuracy_mean: float
    accuracy_std: float
    recall_mean: float
    recall_std: float
    precision_mean: float
    precision_std: float
    f_measure_mean: float
    f_measure_std: float
    specificity_mean: float
    specificity_std: float
    tp_rate_mean: float
    tp_rate_std: float
    fp_rate_mean: float
    fp_rate_std: float

    @classmethod
    def from_evaluations(cls, evaluations: list[Evaluation]) -> Self:
        return cls(
            accuracy_mean=mean(e.accuracy for e in evaluations),
            accuracy_std=stdev(e.accuracy for e in evaluations),
            recall_mean=mean(e.recall for e in evaluations),
            recall_std=stdev(e.recall for e in evaluations),
            precision_mean=mean(e.precision for e in evaluations),
            precision_std=stdev(e.precision for e in evaluations),
            f_measure_mean=mean(e.f_measure for e in evaluations),
            f_measure_std=stdev(e.f_measure for e in evaluations),
            specificity_mean=mean(e.specificity for e in evaluations),
            specificity_std=stdev(e.specificity for e in evaluations),
            tp_rate_mean=mean(e.tp_rate for e in evaluations),
            tp_rate_std=stdev(e.tp_rate for e in evaluations),
            fp_rate_mean=mean(e.fp_rate for e in evaluations),
            fp_rate_std=stdev(e.fp_rate for e in evaluations)
        )
