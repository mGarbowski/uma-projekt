from pprint import pprint
from typing import Type

from src.classifiers.classifier import Classifier
from src.classifiers.id3 import ID3Classifier
from src.classifiers.one_vs_one import OneVsOneClassifier
from src.classifiers.one_vs_rest import OneVsRestClassifier
from src.dataset.dataset import Dataset
from src.evaluation.confusion_matrix import ConfusionMatrix
from src.evaluation.kcv import kcv


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

    datasets = [(car_evaluation, "car evaluation"), (nursery, "nursery"), (balance_scale, "balance scale")]
    models = [ID3Classifier, OneVsRestClassifier, OneVsOneClassifier]

    for named_dataset in datasets:
        dataset, dataset_name = named_dataset
        for model in models:
            print(f"Model: {model.__name__}, Dataset: {dataset_name}")
            micro, macro = kcv(model, dataset, 5)
            print(f"Micro-averaged results: {micro}")
            print(f"Macro-averaged results: {macro}")
            print("")


if __name__ == '__main__':
    main()
