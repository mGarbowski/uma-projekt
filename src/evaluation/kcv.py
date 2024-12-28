from typing import Type

from src.classifiers.classifier import Classifier
from src.dataset.dataset import Dataset
from src.evaluation.aggregate_evaluation import AggregateEvaluation
from src.evaluation.confusion_matrix import ConfusionMatrix
from src.evaluation.evaluation import Evaluation


def kcv(model_class: Type[Classifier], dataset: Dataset, k: int) -> tuple[AggregateEvaluation, AggregateEvaluation]:
    """K-fold cross-validation for a given model and dataset

    Aggregates results by macro-averaging evaluations over all folds
    Returns 2 aggregate evaluations: one for micro-averaged results (in a single fold) and one for macro-averaged results
    """
    evaluations_micro = []
    evaluations_macro = []
    dataset.shuffle()
    for i in range(k):
        train_set, test_set = dataset.kcv_split(k, i)
        model = model_class.train(train_set)
        predictions = model.predict(test_set.attributes)

        confusion_matrix = ConfusionMatrix.from_labels(test_set.labels, predictions)
        evaluations_micro.append(Evaluation.micro_average(confusion_matrix))
        evaluations_macro.append(Evaluation.macro_average(confusion_matrix))

    micro_aggregate = AggregateEvaluation.from_evaluations(evaluations_micro)
    macro_aggregate = AggregateEvaluation.from_evaluations(evaluations_macro)
    return micro_aggregate, macro_aggregate
