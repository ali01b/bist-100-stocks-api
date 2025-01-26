def calculate_strong_support_resistance(data):
    pivots = []
    for i in range(2, len(data) - 2):
        if data['High'][i] > data['High'][i - 1] and data['High'][i] > data['High'][i - 2] and \
           data['High'][i] > data['High'][i + 1] and data['High'][i] > data['High'][i + 2]:
            pivots.append((data['High'][i], 'resistance'))

        if data['Low'][i] < data['Low'][i - 1] and data['Low'][i] < data['Low'][i - 2] and \
           data['Low'][i] < data['Low'][i + 1] and data['Low'][i] < data['Low'][i + 2]:
            pivots.append((data['Low'][i], 'support'))

    return pivots
