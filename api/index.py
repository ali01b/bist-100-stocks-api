
import yfinance as yf
from flask import Flask, jsonify, render_template


## Calculates
from calculators.support_resistance import calculate_support_resistance
from calculators.indicators.macd import calculate_macd 
from calculators.indicators.rsi import calculate_rsi 



app = Flask(__name__, template_folder="template", static_folder="static")


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chart')
def chart():
    return render_template("chart.html")

@app.route('/api/stock/<string:symbol>', methods=['GET'])
def stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        
        # Short-term support and resistance ( 1months)
        levels_1m = stock.history(period="1mo")
        levels_1m_support, levels_1m_resistance = calculate_support_resistance(levels_1m)
        
        # Short-term support and resistance (3 months)
        levels_3m = stock.history(period="3mo")
        levels_3m_support, levels_3m_resistance = calculate_support_resistance(levels_3m)

        # Long-term support and resistance (6 months)
        levels_6m = stock.history(period="6mo")
        levels_6m_support, levels_6m_resistance = calculate_support_resistance(levels_6m)
        
        # Long-term support and resistance (12 months)
        levels_1y = stock.history(period="1y")
        levels_1y_support, levels_1y_resistance = calculate_support_resistance(levels_6m)
        
        levels_2y = stock.history(period="2y")
        levels_2y_support, levels_2y_resistance = calculate_support_resistance(levels_6m)
        
        stock_data = yf.download(symbol, period="2y", interval="1h")

        if stock_data.empty:
            return jsonify({"error": "Veri bulunamadı"}), 404

        stock_data.reset_index(inplace=True)
        stock_data["time"] = stock_data["Datetime"].dt.tz_convert("UTC").astype("int64") // 10**9
        
        stock_data_with_rsi = calculate_rsi(stock_data, period=14)
        stock_data_with_macd = calculate_macd(stock_data_with_rsi)


        # Current price
        recent_data = stock.history(period="1d")
        if not recent_data.empty:
            current_price = round(recent_data['Close'].iloc[-1], 2)
        else:
            current_price = None

        # Historical data (12 months)
        historical_data = []
        for index, row in levels_2y.iterrows():
            historical_data.append({
                "time": index.strftime('%Y-%m-%d'),
                "open": round(row['Open'], 2),
                "high": round(row['High'], 2),
                "low": round(row['Low'], 2),
                "close": round(row['Close'], 2)
            })
            
        response = {
            "symbol": symbol.upper().replace(".IS", ""),
            "current_price": current_price,
            "levels": {
            "1_mo": {
                "support": levels_1m_support,
                "resistance": levels_1m_resistance,
            },
            "3_mo": {
                "support": levels_3m_support,
                "resistance": levels_3m_resistance,
            },
            "6_mo": {
                "support": levels_6m_support,
                "resistance": levels_6m_resistance,
            },
            "1_year": {
                "support": levels_1y_support,
                "resistance": levels_1y_resistance,
            },
            "2_year": {
                "support": levels_2y_support,
                "resistance": levels_2y_resistance,
            },
            },
            "indicators": {
                "rsi": stock_data_with_rsi[["time", "rsi"]].dropna().to_dict(orient="records"),
                # "macd": macd,
                # "signal": signal
            },
            "historical_data": historical_data
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)