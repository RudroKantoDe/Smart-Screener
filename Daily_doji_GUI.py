import pandas as pd
from check_doji import doji
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent 
el = BASE_DIR / 'EQUITY_L.CSV'

equity_details = pd.read_csv(el)
symbol_map = dict(zip(equity_details.SYMBOL, equity_details["NAME OF COMPANY"]))

def check_doji():
    results = []

    for name in equity_details.SYMBOL:
        try:
            nam = name+'.csv'
            data_dir = BASE_DIR / 'data' / nam
            stock_details = pd.read_csv(data_dir)
            data = stock_details.tail(2)  # Use last 2 rows for % change

            if len(data) < 2:
                continue

            opn = data.iloc[-1].Open
            close = data.iloc[-1].Close
            high = data.iloc[-1].High
            low = data.iloc[-1].Low
            volume = data.iloc[-1].Volume

            prev_close = data.iloc[-2].Close
            percent_change = ((close - prev_close) / prev_close) * 100

            dj = [opn, low, high, close]
            dj = list(map(float, dj))
            dj = list(map(int, dj))

            if volume >= 200000 and close >= 100:
                if doji(dj) == 1:
                    pattern = "Green Doji"
                elif doji(dj) == 2:
                    pattern = "Red Doji"
                else:
                    continue

                company_name = symbol_map.get(name, name)#Mapping to actaul comnay name column
                results.append((name, company_name, f"{close:.2f}", f"{percent_change:+.2f}%", pattern))

        except Exception as e:
            print(f'{name} --> {e}')

    return results

