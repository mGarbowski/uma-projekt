from itertools import combinations
from typing import Self

from ..classifiers.classifier import Classifier
from ..dataset.dataset import RowAttributes, Label, Dataset

def get_pairs(labels: set[Label]) -> list[tuple[Label, Label]]:
    return list(combinations(labels, 2))

class OneVsOneClassifier(Classifier):
    @classmethod
    def train(cls, dataset: Dataset) -> Self:
        pass

    def predict_single(self, row_attributes: RowAttributes) -> Label:
        pass
