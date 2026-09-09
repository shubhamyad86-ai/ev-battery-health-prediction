"""
=========================================================
EV Battery Health Analytics
metrics.py

Calculates regression evaluation metrics
=========================================================
"""

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error,
    median_absolute_error,
    explained_variance_score,
    max_error
)

import numpy as np


def evaluate(y_true, y_pred):
    """
    Calculate regression evaluation metrics.
    """

    mae = mean_absolute_error(y_true, y_pred)

    mse = mean_squared_error(y_true, y_pred)

    rmse = np.sqrt(mse)

    r2 = r2_score(y_true, y_pred)

    mape = mean_absolute_percentage_error(y_true, y_pred)

    medae = median_absolute_error(y_true, y_pred)

    evs = explained_variance_score(y_true, y_pred)

    maxerr = max_error(y_true, y_pred)

    mbe = np.mean(y_pred - y_true)

    return {

        "MAE": mae,

        "MSE": mse,

        "RMSE": rmse,

        "R2": r2,

        "MAPE": mape,

        "MedianAE": medae,

        "ExplainedVariance": evs,

        "MaxError": maxerr,

        "MeanBiasError": mbe

    }