import pandas_ta as ta
def calculate_rsi(data, period=14):
    data["rsi"] = ta.rsi(data["Close"], length=period)
    return data