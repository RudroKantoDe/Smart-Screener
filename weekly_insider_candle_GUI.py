import pandas as pd
import datetime as d
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
el = BASE_DIR / 'EQUITY_L.CSV'

equity_details = pd.read_csv(el)
symbol_map = dict(zip(equity_details.SYMBOL, equity_details["NAME OF COMPANY"]))

def check_insider():
    results = []

    for name in equity_details.SYMBOL:
        try:
            nam = name+'.csv'
            data_dir = BASE_DIR / 'data' / nam
            stock_details = pd.read_csv(data_dir)
            stock_details['Price'] = pd.to_datetime(stock_details['Price'], format='%Y-%m-%d')

            today = pd.Timestamp('today')
            previous_monday = today - pd.Timedelta(days=(today.weekday() + 7) % 7)
            pre_previous_monday = previous_monday - pd.Timedelta(days=7)

            previous_monday = previous_monday.strftime('%Y-%m-%d')
            pre_previous_monday = pre_previous_monday.strftime('%Y-%m-%d')

            cur_week_values = stock_details[stock_details['Price'] >= previous_monday]
            pre_week_values = stock_details[(stock_details['Price'] >= pre_previous_monday) & (stock_details['Price'] < previous_monday)]

            if len(cur_week_values) < 2 or len(pre_week_values) < 2:
                continue

            # Extract previous week data
            pre_week_high = float(pre_week_values['High'].max())
            pre_week_low = float(pre_week_values['Low'].min())
            pre_week_open = float(pre_week_values.head(1)['Open'].iloc[0])
            pre_week_close = float(pre_week_values.tail(1)['Close'].iloc[0])

            # Extract current week data
            cur_week_high = float(cur_week_values['High'].max())
            cur_week_low = float(cur_week_values['Low'].min())
            cur_week_open = float(cur_week_values.head(1)['Open'].iloc[0])
            cur_week_close = float(cur_week_values.tail(1)['Close'].iloc[0])
            volume = cur_week_values['Volume'].mean()

            company_name = symbol_map.get(name, name)
            pattern = None

            if (pre_week_open > pre_week_close and cur_week_open < cur_week_close and
                cur_week_open > pre_week_close and cur_week_close < pre_week_open and
                pre_week_high > cur_week_high and pre_week_low < cur_week_low and
                volume > 200000 and cur_week_close >= 100):
                pattern = "Green Insider Candle"

            elif (pre_week_close > pre_week_open and cur_week_open > cur_week_close and
                  pre_week_open < cur_week_close and cur_week_open < pre_week_close and
                  pre_week_high > cur_week_high and pre_week_low < cur_week_low and
                  volume > 200000 and cur_week_close >= 100):
                pattern = "Red Insider Candle"

            if pattern:
                percent_change = ((cur_week_close - pre_week_close) / pre_week_close) * 100
                results.append((name, company_name, f"{cur_week_close:.2f}", f"{percent_change:+.2f}%", pattern))

        except Exception as e:
            print(f"{name} --> {e}")

    return results


