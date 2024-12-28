from typing import Self

from .classifier import Classifier
from .id3 import ID3Classifier
from ..dataset.dataset import RowAttributes, Label, Dataset


class OneVsRestClassifier(Classifier):
    """One vs Rest Classifier

    An ensemble classifier that trains a separate ID3 tree for each class in the dataset.
    Each tree is trained to predict whether a data point belongs to the class or not.
    The positive prediction with the highest weight is chosen as the final prediction.
    If no positive prediction is made, the negative prediction with the lowest weight is chosen.
    """

    _trees: dict[Label, ID3Classifier]

    def __init__(self, trees: dict[Label, ID3Classifier]):
        self._trees = trees

    @classmethod
    def train(cls, dataset: Dataset) -> Self:
        trees = {}
        for label in dataset.unique_labels():
            binarized_dataset = dataset.binarize_labels(label)
            tree = ID3Classifier.train(binarized_dataset)
            trees[label] = tree
        return cls(trees)

    def predict_single(self, row_attributes: RowAttributes) -> Label:
        predictions = {label: tree.predict_single_with_weight(row_attributes) for label, tree in self._trees.items()}
        positive_predictions = {label: pred for label, pred in predictions.items() if pred[0] == label}

        if len(positive_predictions) == 0:
            return min(predictions, key=lambda k: predictions[k][1])[0]

        return max(positive_predictions, key=lambda k: positive_predictions[k][1])[0]
