from typing import Self

from ..classifiers.classifier import Classifier
from ..dataset.dataset import RowAttributes, Label, Dataset


class OneVsOneClassifier(Classifier):
    @classmethod
    def train(cls, dataset: Dataset) -> Self:
        pass

    def predict_single(self, row_attributes: RowAttributes) -> Label:
        pass
