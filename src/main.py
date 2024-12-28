from pprint import pprint

from classifiers.dataset import Dataset
from classifiers.id3 import ID3Classifier
from evaluation.confusion_matrix import ConfusionMatrix


def main():
    car_evaluation = Dataset.load_from_file("datasets/car+evaluation/car.data")
    nursery = Dataset.load_from_file("datasets/nursery/nursery.data")
    balance_scale = Dataset.load_from_file("datasets/balance+scale/balance-scale.data")

    model = ID3Classifier.train(car_evaluation)
    predictions = model.predict(car_evaluation.attributes)
    actual_labels = car_evaluation.labels
    confusion_matrix = ConfusionMatrix.from_labels(actual_labels, predictions)
    pprint(confusion_matrix.matrix)


if __name__ == '__main__':
    main()
