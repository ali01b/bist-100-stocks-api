import numpy as np

def calculate_support_resistance(data):
    highs = data['High']
    lows = data['Low']

    high_mean = np.mean(highs)
    low_mean = np.mean(lows)

    resistance = max(highs[highs > high_mean].tail(3))
    support = min(lows[lows < low_mean].tail(3))

    return round(support, 2), round(resistance, 2)