import random
from typing import Self, Iterable

RowAttributes = tuple[str, ...]
Label = str


class Dataset:
    """Represents a dataset

    A single datapoint is represented by a tuple of attributes and a class
    tuple and class are located at corresponding indices in the lists
    All attributes and classes are strings

    attributes and classes are of equal length
    """
    _attributes: list[RowAttributes]
    _labels: list[Label]

    def __init__(self, attributes: list[RowAttributes] = None, labels: list[Label] = None):
        if attributes is None and labels is None:
            self._attributes = []
            self._labels = []
            return

        if len(attributes) != len(labels):
            raise ValueError("Attributes and labels must have equal length")

        self._attributes = attributes if attributes is not None else []
        self._labels = labels if labels is not None else []

    def __eq__(self, other: Self) -> bool:
        return self.attributes == other.attributes and self.labels == other.labels

    def __getitem__(self, index: int) -> tuple[RowAttributes, Label]:
        return self._attributes[index], self._labels[index]

    @property
    def attributes(self) -> list[RowAttributes]:
        return self._attributes

    @property
    def labels(self) -> list[Label]:
        return self._labels

    def is_empty(self) -> bool:
        return len(self._attributes) == 0

    def size(self):
        return len(self._attributes)

    def add_row(self, row_attributes: RowAttributes, row_label: Label):
        self._attributes.append(row_attributes)
        self._labels.append(row_label)

    def split_by_attribute(self, attribute_idx: int) -> list[Self]:
        unique_attribute_values = set(data_point[attribute_idx] for data_point in self._attributes)
        new_datasets = {attr_value: Dataset() for attr_value in unique_attribute_values}

        for row_attributes, row_label in zip(self._attributes, self._labels):
            split_attribute = row_attributes[attribute_idx]
            new_datasets[split_attribute].add_row(row_attributes, row_label)

        return list(new_datasets.values())

    def train_test_split(self, train_ratio: float = 0.6) -> tuple[Self, Self]:
        if train_ratio < 0 or train_ratio > 1:
            raise ValueError("train_ratio must be between 0 and 1")

        train_size = int(self.size() * train_ratio)
        idxs = set(range(self.size()))
        train_idxs = set(random.sample(list(idxs), train_size))
        test_idxs = idxs.difference(train_idxs)

        train_dataset = Dataset()
        for idx in train_idxs:
            attrs, label = self[idx]
            train_dataset.add_row(attrs, label)

        test_dataset = Dataset()
        for idx in test_idxs:
            attrs, label = self[idx]
            test_dataset.add_row(attrs, label)

        return train_dataset, test_dataset

    def binarize_labels(self, positive_label: str) -> Self:
        new_labels = [positive_label if label == positive_label else "other" for label in self.labels]
        return Dataset(self.attributes, new_labels)

    def unique_labels(self) -> set[Label]:
        return set(self.labels)

    def subset_with_labels(self, labels: Iterable[Label]) -> Self:
        new_attributes = []
        new_labels = []
        for attrs, label in zip(self.attributes, self.labels):
            if label in labels:
                new_attributes.append(attrs)
                new_labels.append(label)

        return Dataset(new_attributes, new_labels)

    @classmethod
    def load_from_file(cls, file_path: str, label_col_idx: int = 0) -> Self:
        with open(file_path, mode="rt", encoding="utf-8") as file:
            lines = file.readlines()
            attributes = []
            labels = []
            for line in lines:
                values = line.strip().split(",")
                label = values.pop(label_col_idx)
                attrs = tuple(values)
                attributes.append(attrs)
                labels.append(label)

            return cls(attributes, labels)
