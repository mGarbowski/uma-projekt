from pprint import pprint
from typing import Type

from src.classifiers.classifier import Classifier
from src.classifiers.id3 import ID3Classifier
from src.classifiers.one_vs_one import OneVsOneClassifier
from src.classifiers.one_vs_rest import OneVsRestClassifier
from src.classifiers.random_classifier import RandomClassifier
from src.dataset.dataset import Dataset
from src.evaluation.confusion_matrix import ConfusionMatrix
from src.evaluation.kcv import kcv


def test_model_on_dataset(model_class: Type[Classifier], dataset: Dataset):
    model = model_class.train(dataset)
    predictions = model.predict(dataset.attributes)
    actual_labels = dataset.labels
    confusion_matrix = ConfusionMatrix.from_labels(actual_labels, predictions)
    pprint(confusion_matrix.matrix)


def experiment_train_test_split():
    dataset = Dataset.load_from_file("datasets/balance+scale/balance-scale.data")
    train_set, test_set = dataset.train_test_split(0.6)
    model = ID3Classifier.train(train_set)
    predictions = model.predict(test_set.attributes)
    confusion_matrix = ConfusionMatrix.from_labels(test_set.labels, predictions)
    pprint(confusion_matrix.matrix)

    micro, macro = kcv(ID3Classifier, dataset, 5)
    print(f"Micro-averaged results: {micro}")
    print(f"Macro-averaged results: {macro}")


def main():
    car_evaluation = Dataset.load_from_file("datasets/car+evaluation/car.data", label_col_idx=6)
    nursery = Dataset.load_from_file("datasets/nursery/nursery.data", label_col_idx=8)
    balance_scale = Dataset.load_from_file("datasets/balance+scale/balance-scale.data", label_col_idx=0)

    datasets = [
        car_evaluation,
        nursery,
        balance_scale,
    ]
    models = [RandomClassifier, ID3Classifier, OneVsRestClassifier, OneVsOneClassifier]

    for dataset in datasets:
        for model in models:
            print(f"Model: {model.__name__}, Dataset: {dataset.name}")
            micro, macro = kcv(model, dataset, 5)
            print(f"Micro-averaged results: {micro}")
            print(f"Macro-averaged results: {macro}")
            print("")


if __name__ == '__main__':
    main()
    # experiment_train_test_split()