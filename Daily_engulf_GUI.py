import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
el = BASE_DIR / 'EQUITY_L.CSV'

equity_details = pd.read_csv(el)
symbol_map = dict(zip(equity_details.SYMBOL, equity_details["NAME OF COMPANY"]))

def check_engulfing():
    results = []

    for name in equity_details.SYMBOL:
        try:
            nam = name+'.csv'
            data_dir = BASE_DIR / 'data' / nam
            stock_details = pd.read_csv(data_dir)
            data = stock_details.tail(2)

            if len(data) < 2:
                continue

            prev = data.iloc[0]
            curr = data.iloc[1]

            pclose = float(prev['Close'])
            popen = float(prev['Open'])
            cclose = float(curr['Close'])
            copen = float(curr['Open'])
            volume = float(curr['Volume'])

            pattern = None

            # Bullish Engulfing
            if (popen > pclose and copen < cclose and copen < pclose and cclose > popen and
                volume >= 200000 and cclose >= 100):
                pattern = "Bullish Engulfing"

            # Bearish Engulfing
            elif (pclose > popen and copen > cclose and popen > cclose and copen > pclose and
                  volume >= 200000 and cclose >= 100):
                pattern = "Bearish Engulfing"

            if pattern:
                company = symbol_map.get(name, name)
                percent_change = ((cclose - pclose) / pclose) * 100
                results.append((name, company, f"{cclose:.2f}", f"{percent_change:+.2f}%", pattern))

        except Exception as e:
            print(f"{name} --> {e}")

    return results


