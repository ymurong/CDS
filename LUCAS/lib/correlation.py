import scipy.stats as ss
import pandas as pd
import numpy as np


def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    chi2, p, dof, ex = ss.chi2_contingency(confusion_matrix)
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1))),


def cramer_v_matrix(data: pd.DataFrame):
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
