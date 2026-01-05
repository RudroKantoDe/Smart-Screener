import pandas as pd
from datetime import datetime, timedelta
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
            stock_details['Price'] = pd.to_datetime(stock_details['Price'], format='%Y-%m-%d')

            today = pd.Timestamp('today')
            previous_monday = today - pd.Timedelta(days=(today.weekday() + 7) % 7)
            pre_previous_monday = previous_monday - pd.Timedelta(days=7)

            previous_monday_str = previous_monday.strftime('%Y-%m-%d')
            pre_previous_monday_str = pre_previous_monday.strftime('%Y-%m-%d')

            cur_week_values = stock_details[stock_details['Price'] >= previous_monday_str]
            pre_week_values = stock_details[(stock_details['Price'] >= pre_previous_monday_str) & (stock_details['Price'] < previous_monday_str)]

            if len(cur_week_values) < 2 or len(pre_week_values) < 2:
                continue

            pre_week_open = float(pre_week_values.iloc[0]['Open'])
            pre_week_close = float(pre_week_values.iloc[-1]['Close'])

            cur_week_open = float(cur_week_values.iloc[0]['Open'])
            cur_week_close = float(cur_week_values.iloc[-1]['Close'])

            volume = cur_week_values['Volume'].mean()
            pattern = None

            # Bullish Engulfing
            if (pre_week_open > pre_week_close and cur_week_open < cur_week_close and
                cur_week_open < pre_week_close and cur_week_close > pre_week_open and
                volume >= 200000 and cur_week_close >= 100):
                pattern = "Bullish Engulfing"

            # Bearish Engulfing
            elif (pre_week_close > pre_week_open and cur_week_open > cur_week_close and
                  pre_week_open > cur_week_close and cur_week_open > pre_week_close and
                  volume >= 200000 and cur_week_close >= 100):
                pattern = "Bearish Engulfing"

            if pattern:
                company_name = symbol_map.get(name, name)
                percent_change = ((cur_week_close - pre_week_close) / pre_week_close) * 100
                results.append((name, company_name, f"{cur_week_close:.2f}", f"{percent_change:+.2f}%", pattern))

        except Exception as e:
            print(f"{name} --> {e}")

    return results




