from pprint import pprint

from classifiers.id3 import ID3Classifier
from dataset.dataset import Dataset
from evaluation.confusion_matrix import ConfusionMatrix


def test_on_dataset(dataset: Dataset):
    model = ID3Classifier.train(dataset)
    predictions = model.predict(dataset.attributes)
    actual_labels = dataset.labels
    confusion_matrix = ConfusionMatrix.from_labels(actual_labels, predictions)
    pprint(confusion_matrix.matrix)


def main():
    car_evaluation = Dataset.load_from_file("datasets/car+evaluation/car.data")
    nursery = Dataset.load_from_file("datasets/nursery/nursery.data")
    balance_scale = Dataset.load_from_file("datasets/balance+scale/balance-scale.data")

    test_on_dataset(car_evaluation)
    test_on_dataset(nursery)
    test_on_dataset(balance_scale)


if __name__ == '__main__':
    main()
