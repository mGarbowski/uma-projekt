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


def generate_csv_report(filename, models, datasets):
    with open(filename, "w") as f:
        f.write(
            "model,dataset,averaging_mode,accuracy_mean,accuracy_std,recall_mean,recall_std,precision_mean,precision_std,f_measure_mean,f_measure_std,specificity_mean,specificity_std,tp_rate_mean,tp_rate_std,fp_rate_mean,fp_rate_std\n")
        for dataset in datasets:
            for model in models:
                micro, macro = kcv(model, dataset, 5)
                f.write(
                    f"{model.__name__},{dataset.name},micro,{micro.accuracy_mean:.3f},{micro.accuracy_std:.3f},{micro.recall_mean:.3f},{micro.recall_std:.3f},{micro.precision_mean:.3f},{micro.precision_std:.3f},{micro.f_measure_mean:.3f},{micro.f_measure_std:.3f},{micro.specificity_mean:.3f},{micro.specificity_std:.3f},{micro.tp_rate_mean:.3f},{micro.tp_rate_std:.3f},{micro.fp_rate_mean:.3f},{micro.fp_rate_std:.3f}\n")
                f.write(
                    f"{model.__name__},{dataset.name},macro,{macro.accuracy_mean:.3f},{macro.accuracy_std:.3f},{macro.recall_mean:.3f},{macro.recall_std:.3f},{macro.precision_mean:.3f},{macro.precision_std:.3f},{macro.f_measure_mean:.3f},{macro.f_measure_std:.3f},{macro.specificity_mean:.3f},{macro.specificity_std:.3f},{macro.tp_rate_mean:.3f},{macro.tp_rate_std:.3f},{macro.fp_rate_mean:.3f},{macro.fp_rate_std:.3f}\n")

def main():
    datasets = [
        Dataset.load_from_file("datasets/car+evaluation/car.data", label_col_idx=6),
        Dataset.load_from_file("datasets/balance+scale/balance-scale.data", label_col_idx=0),
        Dataset.load_from_file("datasets/national+poll+on+healthy+aging+(npha)/NPHA-doctor-visits.csv", label_col_idx=0)
    ]

    models = [
        ID3Classifier,
        OneVsRestClassifier,
        OneVsOneClassifier
    ]

    generate_csv_report("results.csv", models, datasets)


if __name__ == '__main__':
    main()
