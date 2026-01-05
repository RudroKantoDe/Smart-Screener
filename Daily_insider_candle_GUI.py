import pandas as pd
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
            data = stock_details.tail(2)
            pddata = data.head(1).values.tolist()
            cddata = data.tail(1).values.tolist()

            pclose = pddata[0][1]
            popen = pddata[0][4]
            phigh = pddata[0][2]
            plow = pddata[0][3]

            cclose = cddata[0][1]
            copen = cddata[0][4]
            chigh = cddata[0][2]
            clow = cddata[0][3]
            volume = cddata[0][5]

            company_name = symbol_map.get(name, name)
            pattern = None

            if (popen > pclose and copen < cclose and copen > pclose and cclose < popen and
                phigh > chigh and plow < clow and volume >= 200000 and cclose >= 100):
                pattern = "Green Insider Candle"

            elif (pclose > popen and copen > cclose and popen < cclose and copen < pclose and
                  phigh > chigh and plow < clow and volume >= 200000 and cclose >= 100):
                pattern = "Red Insider Candle"

            if pattern:
                results.append((name, company_name, f"{cclose:.2f}", f"{((cclose - pclose) / pclose * 100):+.2f}%", pattern))

        except Exception as e:
            print(f"{name} --> {e}")

    return results



