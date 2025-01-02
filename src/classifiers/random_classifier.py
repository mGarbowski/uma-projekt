import random
from typing import Self

from src.classifiers.classifier import Classifier
from src.dataset.dataset import Label, RowAttributes


class RandomClassifier(Classifier):
    unique_labels: list[Label]

    def __init__(self, unique_labels: list[Label]):
        self.unique_labels = unique_labels

    @classmethod
    def train(cls, dataset) -> Self:
        return cls(list(dataset.unique_labels()))

    def predict_single(self, row_attributes: RowAttributes) -> Label:
        return random.choice(self.unique_labels)