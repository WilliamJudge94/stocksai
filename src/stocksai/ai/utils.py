import numpy as np
from numpy.lib.stride_tricks import as_strided

def rolling_window(a, window_length):
    shape = (a.shape[0] - window_length + 1, window_length, 1)
    strides = (a.strides[0], a.strides[0], a.itemsize)
    return as_strided(a, shape=shape, strides=strides)

def normalize(array):
    min_val = np.min(array)
    max_val = np.max(array)
    return (array - min_val) / (max_val - min_val)

def anomaly_prep(data, window_length):
    data = normalize(data)
    data = rolling_window(data, window_length)
    normalized_inputs = np.array([normalize(window) for window in data])
    return normalized_inputs