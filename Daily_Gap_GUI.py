import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
el = BASE_DIR / 'EQUITY_L.CSV'

equity_details = pd.read_csv(el)
symbol_map = dict(zip(equity_details.SYMBOL, equity_details["NAME OF COMPANY"]))

def check_gap_up():
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

            cur_open = float(curr['Open'])
            cur_close = float(curr['Close'])
            cur_low = float(curr['Low'])
            cur_vol = float(curr['Volume'])
            pre_high = float(prev['High'])

            if cur_open > pre_high and cur_low > pre_high and cur_close > cur_open and cur_vol > 300000:
                company = symbol_map.get(name, name)
                change = ((cur_close - prev['Close']) / prev['Close']) * 100
                results.append((name, company, f"{cur_close:.2f}", f"{change:+.2f}%", "Gap Up"))

        except Exception as e:
            print(f"{name} --> {e}")

    return results

def check_gap_down():
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

            cur_open = float(curr['Open'])
            cur_close = float(curr['Close'])
            cur_high = float(curr['High'])
            cur_vol = float(curr['Volume'])
            pre_low = float(prev['Low'])

            if cur_open < pre_low and cur_high < pre_low and cur_close < cur_open and cur_vol > 300000:
                company = symbol_map.get(name, name)
                change = ((cur_close - prev['Close']) / prev['Close']) * 100
                results.append((name, company, f"{cur_close:.2f}", f"{change:+.2f}%", "Gap Down"))

        except Exception as e:
            print(f"{name} --> {e}")

    return results


