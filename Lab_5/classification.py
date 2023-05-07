from typing import List, Tuple


def get_confusion_matrix(
    y_true: List[int], y_pred: List[int], num_classes: int,
) -> List[List[int]]:
    """
    Generate a confusion matrix in a form of a list of lists. 

    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values
    :param num_classes: number of supported classes

    :return: confusion matrix
    """
    if (len(y_true) != len(y_pred)):
        raise ValueError("Invalid input shapes!")
    # if (all([0 <= elem_1 < num_classes and 0 <= elem_2 < num_classes for (elem_1, elem_2) in zip(y_true, y_pred)])):
    #     raise ValueError("Invalid prediction classes!")
    if not(all([0 <= elem < num_classes for elem in y_pred])):
        raise ValueError("Invalid prediction classes!")

    cm = []
    length = len(y_true)
    for class_index in range(num_classes):
        class_conf_list = [sum((1 for j in range(length) if y_true[j]==class_index and y_pred[j]==compared_class)) for compared_class in range(num_classes)]
        cm.append(class_conf_list)
    return cm


def get_quality_factors(
    y_true: List[int],
    y_pred: List[int],
) -> Tuple[int, int, int, int]:
    """
    Calculate True Negative, False Positive, False Negative and True Positive 
    metrics basing on the ground truth and predicted lists.

    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: a tuple of TN, FP, FN, TP
    """
    control_list = [(elem_true - elem_pred, elem_true * elem_pred) for (elem_true, elem_pred) in zip(y_true, y_pred)]
    TN = sum((1 for diff_prod_tuple in control_list if diff_prod_tuple==(0,0)))
    FP = sum((1 for diff_prod_tuple in control_list if diff_prod_tuple==(-1,0)))
    FN = sum((1 for diff_prod_tuple in control_list if diff_prod_tuple==(1,0)))
    TP = sum((1 for diff_prod_tuple in control_list if diff_prod_tuple==(0,1)))

    return (TN, FP, FN, TP)


def accuracy_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the accuracy for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: accuracy score
    """
    
    """
    Accuracy is how close a given set of measurements (observations or readings)
    are to their true value.
    """
    (TN, FP, FN, TP) = get_quality_factors(y_true, y_pred)
    ACC = (TP + TN) / sum((TN, FP, FN, TP))
    return ACC


def precision_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the precision for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: precision score
    """

    """
    The positive predictive value (PPV) is the proportion 
    of true positives and the sum of true positives and false positives.
    """

    (TN, FP, FN, TP) = get_quality_factors(y_true, y_pred)
    PPV = TP / (TP + FP)
    return PPV


def recall_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the recall for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: recall score
    """

    """
    The true positive rate (TPR) is the proportion 
    of true positives and the sum of true positives and false negatives.
    """

    (TN, FP, FN, TP) = get_quality_factors(y_true, y_pred)
    TPR = TP / (TP + FN)
    return TPR


def f1_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the F1-score for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: F1-score
    """

    """
    The F1 score is the harmonic mean of the precision and recall.
    It thus symmetrically represents both precision and recall in one metric.
    """
    # PPV = precision_score(y_true, y_pred)
    # TPR = recall_score(y_true, y_pred)
    # F_1 = 2 * ((PPV * TPR) / (PPV + TPR))
    # return F_1
    (TN, FP, FN, TP) = get_quality_factors(y_true, y_pred)
    F_1 = (2 * TP) / (2 * TP + FP + FN)
    return F_1

