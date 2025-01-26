import pandas_ta as ta

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    df = data.copy()
    macd = ta.macd(df["Close"], fast=fast_period, slow=slow_period, signal=signal_period)
    df["macd"] = macd["MACD_12_26_9"]
    df["signal"] = macd["MACDs_12_26_9"]
    df = df.dropna(subset=["macd", "signal"])  # Boş (NaN) değerleri kaldır
    return df