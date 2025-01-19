"""Authors: Mikołaj Garbowski, Michał Pałasz"""

from abc import ABC, abstractmethod
from typing import Self

from src.dataset.dataset import Dataset, Label, RowAttributes


class Classifier(ABC):

    @classmethod
    @abstractmethod
    def train(cls, dataset: Dataset) -> Self:
        pass

    @abstractmethod
    def predict_single(self, row_attributes: RowAttributes) -> Label:
        """Predict label for a single row"""
        pass

    def predict(self, attributes: list[RowAttributes]) -> list[Label]:
        """Predict label based on attributes for each row"""
        return [self.predict_single(row_attributes) for row_attributes in attributes]

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass
