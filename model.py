import numpy as np
import pandas as pd
import matplotlib.pylab as plt

from sklearn.linear_model import RANSACRegressor

from darts.timeseries import TimeSeries
from darts.models import RegressionModel
from darts.dataprocessing.transformers import Scaler, StaticCovariatesTransformer
from darts.metrics import mape

import torch
import pickle

#Custom transformer, likely could be replaced with prexisting one
class ZipfTransformer:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return np.power(X, 1 / self.alpha)

    def inverse_transform(self, X):
        return np.power(X, self.alpha)

def eval_model(model, t_list, v_list):
    scaler = Scaler(ZipfTransformer(2), n_jobs=-1)
    scaled_t_list = scaler.fit_transform(t_list)
    model.fit(scaled_t_list)
    forecast = model.predict(series=scaled_t_list, n=len(v_list[0]))
    forecast = scaler.inverse_transform(forecast)
    print(f"model {model} obtains MAPE: {mape(actual_series=v_list, pred_series=forecast, n_jobs=-1, series_reduction=np.mean):.2f}%")

#parse in heavily pruned timeseries list
with open("pruned_five_timeseries_list_static.pkl", "rb") as file:
    series_list = pickle.load(file)

#splitting data
train_list = []
val_list = []
for series in series_list:
    train, val = series.split_after(pd.Timestamp('20241107'))
    train_list.append(train)
    val_list.append(val)

#Naive implementations for comparison
modelA = GlobalNaiveAggregate(
    input_chunk_length=30,
    output_chunk_length=1
)

modelB = GlobalNaiveDrift(
    input_chunk_length=30,
    output_chunk_length=30
)

#Implementation using SciKit-Learn regression model
modelC = RegressionModel(
    lags=40,
    output_chunk_length=3,
    lags_future_covariates=None,
    lags_past_covariates=None,
    use_static_covariates=True,
    model=RANSACRegressor(max_trials=200, random_state=42)
)


model_list = [modelA, modelB, modelC]
for model in model_list:
    eval_model(model, train_list, val_list)
