"""Authors: Mikołaj Garbowski, Michał Pałasz"""

from src.classifiers.id3 import ID3Classifier
from src.classifiers.one_vs_one import OneVsOneClassifier
from src.classifiers.one_vs_rest import OneVsRestClassifier
from src.dataset.dataset import Dataset
from src.evaluation.kcv import kcv


def generate_csv_report(filename, models, datasets):
    with open(filename, "w") as f:
        f.write(
            "Model,Zbiór danych,Uśrednianie,Dokładność (avg),Dokładność (std),Odzysk (avg),Odzysk (std),Precyzja (avg),Precyzja (std),Miara F (avg),Miara F (std),Specyficzność (avg),Specyficzność (std),TP rate (avg),TP rate (std),FP rate (avg),FP rate (std)\n")
        for dataset in datasets:
            for model in models:
                micro, macro = kcv(model, dataset, 5)
                f.write(
                    f"{model.name()},{dataset.name},micro,{micro.accuracy_mean:.3f},{micro.accuracy_std:.3f},{micro.recall_mean:.3f},{micro.recall_std:.3f},{micro.precision_mean:.3f},{micro.precision_std:.3f},{micro.f_measure_mean:.3f},{micro.f_measure_std:.3f},{micro.specificity_mean:.3f},{micro.specificity_std:.3f},{micro.tp_rate_mean:.3f},{micro.tp_rate_std:.3f},{micro.fp_rate_mean:.3f},{micro.fp_rate_std:.3f}\n")
                f.write(
                    f"{model.name()},{dataset.name},macro,{macro.accuracy_mean:.3f},{macro.accuracy_std:.3f},{macro.recall_mean:.3f},{macro.recall_std:.3f},{macro.precision_mean:.3f},{macro.precision_std:.3f},{macro.f_measure_mean:.3f},{macro.f_measure_std:.3f},{macro.specificity_mean:.3f},{macro.specificity_std:.3f},{macro.tp_rate_mean:.3f},{macro.tp_rate_std:.3f},{macro.fp_rate_mean:.3f},{macro.fp_rate_std:.3f}\n")


def main():
    datasets = [
        Dataset.load_from_file("datasets/car+evaluation/car.data", label_col_idx=6, name="Car"),
        Dataset.load_from_file("datasets/balance+scale/balance-scale.data", label_col_idx=0, name="Balance-scale"),
        Dataset.load_from_file("datasets/primary+tumor/primary-tumor.data", label_col_idx=0, name="Primary tumor"),
    ]

    models = [
        ID3Classifier,
        OneVsRestClassifier,
        OneVsOneClassifier
    ]

    generate_csv_report("results/metrics.csv", models, datasets)


if __name__ == '__main__':
    main()
