"""ID3 decision tree classifier implementation

Based on earlier assignment from course Wstęp do Sztucznej Inteligencji
by Mikołaj Garbowski
"""

import math
from dataclasses import dataclass
from typing import Self

from src.dataset.dataset import Dataset, RowAttributes, Label
from src.classifiers.classifier import Classifier


def entropy(dataset: Dataset) -> float:
    return sum(
        - (label_frequency := dataset.labels.count(unique_label) / dataset.size()) * math.log(label_frequency, 2)
        for unique_label in set(dataset.labels)
    )


def entropy_after_split(dataset: Dataset, split_attribute_idx: int) -> float:
    return sum(
        partitioned_dataset.size() / dataset.size() * entropy(partitioned_dataset)
        for partitioned_dataset
        in dataset.split_by_attribute(split_attribute_idx)
    )


def information_gain(dataset: Dataset, split_attribute_idx: int) -> float:
    return entropy(dataset) - entropy_after_split(dataset, split_attribute_idx)


def best_split_idx(dataset: Dataset, unused_attribute_idxs: set[int]) -> int:
    return max(
        unused_attribute_idxs,
        key=lambda idx: information_gain(dataset, idx)
    )


def most_common_element[T](elements: list[T]) -> tuple[T, float]:
    counts = {}
    for element in elements:
        if element not in counts:
            counts[element] = 1
        else:
            counts[element] += 1

    elem, count = max(counts.items(), key=lambda item: item[1])
    weight = count / len(elements)
    return elem, weight


@dataclass
class Node:
    children: dict[str, Self]
    leaf_label: str | None
    weight: float
    most_common_label: str  # fallback for intermediate nodes with no corresponding children
    split_attribute_idx: int | None

    def is_leaf(self) -> bool:
        return self.leaf_label is not None

    @classmethod
    def leaf(cls, label: str, weight: float) -> Self:
        return cls(
            children={},
            leaf_label=label,
            weight=weight,
            most_common_label=label,
            split_attribute_idx=None,
        )


@dataclass(frozen=True)
class WeightedPrediction:
    label: str
    weight: float


class ID3Classifier(Classifier):
    _root: Node

    def __init__(self, root: Node):
        self._root = root

    @classmethod
    def train(cls, dataset: Dataset) -> Self:
        attribute_idxs = set(range(len(dataset.attributes[0])))
        root = build_decision_tree(dataset, attribute_idxs)
        return cls(root)

    def predict_single_with_weight(self, row_attributes: RowAttributes) -> WeightedPrediction:
        """Predict label based on attributes, include weight of the prediction"""
        node = self._root
        while not node.is_leaf():
            attribute_value = row_attributes[node.split_attribute_idx]
            if attribute_value not in node.children:
                return WeightedPrediction(node.most_common_label, node.weight)

            node = node.children[attribute_value]

        return WeightedPrediction(node.leaf_label, node.weight)

    def predict_single(self, row_attributes: RowAttributes) -> Label:
        return self.predict_single_with_weight(row_attributes).label

    def predict_with_weights(self, attributes: list[RowAttributes]) -> list[WeightedPrediction]:
        """Predict label based on attributes for each row, include weight of the prediction"""
        return [self.predict_single_with_weight(row_attributes) for row_attributes in attributes]


def build_decision_tree(
        training_set: Dataset,
        unused_attribute_idxs: set[int],
) -> Node:
    if training_set.is_empty():
        raise ValueError("Training set cannot be empty")

    _, final_label = training_set[0]
    if all(label == final_label for label in training_set.labels):
        return Node.leaf(final_label, 1.0)

    if len(unused_attribute_idxs) == 0:
        most_common_label, weight = most_common_element(training_set.labels)
        return Node.leaf(most_common_label, weight)

    most_common_label, weight = most_common_element(training_set.labels)
    split_attribute_idx = best_split_idx(training_set, unused_attribute_idxs)
    dataset_partition = training_set.split_by_attribute(split_attribute_idx)
    unused_attribute_idxs.remove(split_attribute_idx)
    children = {
        partitioned_set.attributes[0][split_attribute_idx]: build_decision_tree(
            training_set=partitioned_set,
            unused_attribute_idxs=unused_attribute_idxs.copy(),  # pass down a copy of a mutable set
        )
        for partitioned_set in dataset_partition
    }

    return Node(
        children=children,
        leaf_label=None,
        weight=weight,
        most_common_label=most_common_label,
        split_attribute_idx=split_attribute_idx
    )
