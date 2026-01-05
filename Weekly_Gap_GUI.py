import pandas as pd
from datetime import datetime, timedelta
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
            df = pd.read_csv(data_dir)
            df['Price'] = pd.to_datetime(df['Price'], format='%Y-%m-%d')

            today = pd.Timestamp('today')
            prev_mon = today - pd.Timedelta(days=(today.weekday() + 7) % 7)
            pre_prev_mon = prev_mon - pd.Timedelta(days=7)

            prev_mon_str = prev_mon.strftime('%Y-%m-%d')
            pre_prev_mon_str = pre_prev_mon.strftime('%Y-%m-%d')

            cur_week = df[df['Price'] >= prev_mon_str]
            pre_week = df[(df['Price'] >= pre_prev_mon_str) & (df['Price'] < prev_mon_str)]

            if len(cur_week) < 2 or len(pre_week) < 2:
                continue

            pre_high = float(pre_week['High'].max())
            pre_close = float(pre_week.iloc[-1]['Close'])

            cur_open = float(cur_week.iloc[0]['Open'])
            cur_close = float(cur_week.iloc[-1]['Close'])
            cur_low = float(cur_week['Low'].min())
            cur_vol = cur_week['Volume'].mean()

            if cur_open > pre_high and cur_low > pre_high and cur_close > cur_open and cur_vol >= 300000 and cur_close >= 100:
                company = symbol_map.get(name, name)
                change = ((cur_close - pre_close) / pre_close) * 100
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
            df = pd.read_csv(data_dir)
            df['Price'] = pd.to_datetime(df['Price'], format='%Y-%m-%d')

            today = pd.Timestamp('today')
            prev_mon = today - pd.Timedelta(days=(today.weekday() + 7) % 7)
            pre_prev_mon = prev_mon - pd.Timedelta(days=7)

            prev_mon_str = prev_mon.strftime('%Y-%m-%d')
            pre_prev_mon_str = pre_prev_mon.strftime('%Y-%m-%d')

            cur_week = df[df['Price'] >= prev_mon_str]
            pre_week = df[(df['Price'] >= pre_prev_mon_str) & (df['Price'] < prev_mon_str)]

            if len(cur_week) < 2 or len(pre_week) < 2:
                continue

            pre_low = float(pre_week['Low'].min())
            pre_close = float(pre_week.iloc[-1]['Close'])

            cur_open = float(cur_week.iloc[0]['Open'])
            cur_close = float(cur_week.iloc[-1]['Close'])
            cur_high = float(cur_week['High'].max())
            cur_vol = cur_week['Volume'].mean()

            if cur_open < pre_low and cur_high < pre_low and cur_close < cur_open and cur_vol >= 300000 and cur_close >= 100:
                company = symbol_map.get(name, name)
                change = ((cur_close - pre_close) / pre_close) * 100
                results.append((name, company, f"{cur_close:.2f}", f"{change:+.2f}%", "Gap Down"))

        except Exception as e:
            print(f"{name} --> {e}")

    return results



