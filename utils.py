import numpy as np
import pandas as pd
import scipy


def count_spm(data):
    f, t, Sxx = scipy.signal.spectrogram(np.array(data), 5000, nperseg=1200, noverlap=0)
    ind = (f > 8) & (f < 13)
    mu = Sxx[ind]
    power = pd.Series(np.sum(mu ** 2, axis=0)) ** 0.5
    return power.mean()


def find_min_ampl(data):
    minimum = None
    for i in range(4):
        cur_data = data[i * 2]
        for j in range(4):
            cur_data += data[2 * j + 1]
            res = count_spm(cur_data)
            if minimum is None:
                minimum = res
                continue
            if res < minimum:
                minimum = res
    return minimum


def is_depr(cur_mean, prev_mean):
    print(cur_mean / prev_mean)
    try:
        if cur_mean / prev_mean > 1.5:
            return True
        else:
            return False
    except ZeroDivisionError:
        print("error")
