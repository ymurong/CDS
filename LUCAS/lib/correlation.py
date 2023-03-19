import scipy.stats as ss
import pandas as pd
import numpy as np
from typing import Tuple, List
from collections import Counter


def conditional_chi2_test(data: np.array, i: int, j: int, cond_set: List[int]):
    """
    data needs to be in categorical or binary type
    :param data:
    :param i:
    :param j:
    :param cond_set:
    :return:
    """
    size = data.shape[0]
    mask = np.ones(size).astype(bool)
    # we condition on the first category of all features in cond_set
    for col_idx in cond_set:
        first_cat = list(Counter(data[:, col_idx]).keys())[0]
        mask = mask & (data[:, col_idx] == first_cat)

    # we make sure that data only contains entries that hold the same values for
    # features in cond_set (first category for each feature in this case)
    # Example: if cond_set have A,B features, then filtered data should only contain entries that
    # have A with 0 and B with 0 consistently (assume that 0 is the first category of A and B)
    chi2, p = chi2_test(data[mask][:, i], data[mask][:, j])
    return chi2, p


def conditional_chi2_matrix(data: pd.DataFrame, alpha=0.05, cond_set=[0]) -> np.ndarray[bool]:
    """
        chi2 independency matrix
        :return: numpy matrix of boolean values
            - True: Dependency (Reject Null-Hypothesis)
            - False: Independent (Fail to Reject Null-Hypothesis)
        """
    nb_features = data.shape[1]
    chi2_independency_matrix = np.empty((nb_features, nb_features))
    for i in range(nb_features):
        for j in range(nb_features):
            chi2_independency_matrix[i, j] = conditional_chi2_test(data, i, j, cond_set=cond_set)[1] < alpha
    return chi2_independency_matrix


def chi2_test(x: np.array, y: np.array) -> Tuple:
    """
    chi2 indepency test
    :return: tuple of chi2 score and p-value
    """
    confusion_matrix = pd.crosstab(x, y)
    chi2, p, dof, ex = ss.chi2_contingency(confusion_matrix)
    return chi2, p


def chi2_matrix(data: pd.DataFrame, alpha=0.05) -> np.ndarray[bool]:
    """
        chi2 independency matrix
        :return: numpy matrix of boolean values
            - True: Dependency (Reject Null-Hypothesis)
            - False: Independent (Fail to Reject Null-Hypothesis)
        """
    nb_features = data.shape[1]
    chi2_independency_matrix = np.empty((nb_features, nb_features))
    for i in range(nb_features):
        for j in range(nb_features):
            chi2_independency_matrix[i, j] = chi2_test(data.iloc[:, i], data.iloc[:, j])[1] < alpha
    return chi2_independency_matrix


def cramers_v(x: np.array, y: np.array) -> float:
    confusion_matrix = pd.crosstab(x, y)
    chi2, p, dof, ex = ss.chi2_contingency(confusion_matrix)
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1))),


def cramer_v_matrix(data: pd.DataFrame) -> np.ndarray:
    """
    :param data: panda dataframe
    :return: pairwise cramerv correlation matrix
    """
    nb_features = data.shape[1]
    cramerv_matrix = np.empty((nb_features, nb_features))
    for i in range(nb_features):
        for j in range(nb_features):
            cramerv_matrix[i, j] = cramers_v(data.iloc[:, i], data.iloc[:, j])[0]
    return cramerv_matrix
