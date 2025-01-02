from itertools import combinations
from typing import Self

from src.classifiers.classifier import Classifier
from src.classifiers.id3 import ID3Classifier
from src.dataset.dataset import RowAttributes, Label, Dataset

Pair = tuple[Label, Label]


def get_pairs(labels: set[Label]) -> list[Pair]:
    return list(combinations(labels, 2))


class OneVsOneClassifier(Classifier):
    """One vs One Classifier

    An ensemble classifier that trains a separate ID3 tree for each pair of classes in the dataset.
    Each tree is trained to predict whether a data point belongs to one of the classes in the pair.
    Each tree is trained on a subset of the dataset that only contains the classes in the pair.
    The class with the highest weighted vote is chosen as the final prediction.
    Vote is calculated by summing the weights of the positive predictions and complements to 1 of negative predictions
    for each pair.
    """

    _trees: dict[Pair, ID3Classifier]
    _labels: set[Label]

    def __init__(self, trees: dict[Pair, ID3Classifier], labels):
        self._trees = trees
        self._labels = labels

    @classmethod
    def train(cls, dataset: Dataset) -> Self:
        unique_labels = dataset.unique_labels()
        pairs = get_pairs(unique_labels)
        trees = {
            pair: ID3Classifier.train(dataset.subset_with_labels(pair))
            for pair in pairs
        }
        return cls(trees, unique_labels)

    def predict_single(self, row_attributes: RowAttributes) -> Label:
        votes = {label: 0.0 for label in self._labels}
        for pair, tree in self._trees.items():
            prediction = tree.predict_single_with_weight(row_attributes)
            other_label = pair[1] if prediction.label == pair[0] else pair[0]

            votes[prediction.label] += prediction.weight
            votes[other_label] += (1 - prediction.weight)

        return max(votes, key=lambda label: votes[label])

    @classmethod
    def name(cls) -> str:
        return "One vs One"
