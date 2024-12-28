from pprint import pprint
from typing import Type

from src.classifiers.classifier import Classifier
from src.classifiers.id3 import ID3Classifier
from src.classifiers.one_vs_one import OneVsOneClassifier
from src.classifiers.one_vs_rest import OneVsRestClassifier
from src.dataset.dataset import Dataset
from src.evaluation.confusion_matrix import ConfusionMatrix


def test_model_on_dataset(model_class: Type[Classifier], dataset: Dataset):
    model = model_class.train(dataset)
    predictions = model.predict(dataset.attributes)
    actual_labels = dataset.labels
    confusion_matrix = ConfusionMatrix.from_labels(actual_labels, predictions)
    pprint(confusion_matrix.matrix)


def main():
    car_evaluation = Dataset.load_from_file("datasets/car+evaluation/car.data")
    nursery = Dataset.load_from_file("datasets/nursery/nursery.data")
    balance_scale = Dataset.load_from_file("datasets/balance+scale/balance-scale.data")

    datasets = [car_evaluation, nursery, balance_scale]
    models = [ID3Classifier, OneVsRestClassifier, OneVsOneClassifier]

    for dataset in datasets:
        for model in models:
            print(f"Model: {model.__name__}")
            test_model_on_dataset(model, dataset)
            print("")


if __name__ == '__main__':
    main()
