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
            stock_details['Price'] = pd.to_datetime(stock_details['Price'], format='%Y-%m-%d')

            today = pd.Timestamp('today')
            previous_monday = today - pd.Timedelta(days=(today.weekday() + 7) % 7)
            previous_monday = previous_monday.strftime('%Y-%m-%d')

            weekly_data = stock_details[stock_details['Price'] >= previous_monday]

            if weekly_data.empty or len(weekly_data) < 2:
                continue

            opn = weekly_data.head(1).Open.values[0]
            close = weekly_data.tail(1).Close.values[0]
            high = weekly_data['High'].max()
            low = weekly_data['Low'].min()
            volume = weekly_data['Volume'].sum() / len(weekly_data)

            dj = [opn, low, high, close]
            dj = list(map(float, dj))
            dj = list(map(int, dj))

            if volume >= 300000 and close >= 100:
                pattern = None
                if doji(dj) == 1:
                    pattern = "Green Doji"
                elif doji(dj) == 2:
                    pattern = "Red Doji"

                if pattern:
                    prev_close = stock_details[stock_details['Price'] < previous_monday].tail(1).Close.values
                    if len(prev_close) == 0:
                        continue
                    percent_change = ((close - prev_close[0]) / prev_close[0]) * 100
                    company_name = symbol_map.get(name, name)
  # You can map this to full name if available
                    results.append((name, company_name, f"{close:.2f}", f"{percent_change:+.2f}%", pattern))

        except Exception as e:
            print(f'{name} --> {e}')

    return results




