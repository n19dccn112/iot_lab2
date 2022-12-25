import numpy as np


def format_3d_x(df):
    X = np.array(df)
    o = np.reshape(df, (X.shape[0], X.shape[1]*X.shape[2], 3))
    o = np.asarray(o)
    return o