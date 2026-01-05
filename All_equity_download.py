import pandas as pd
import yfinance as yf
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent 
el = BASE_DIR / 'EQUITY_L.CSV'

def datadownload():
  equity_details = pd.read_csv(el)  
  for name in equity_details.SYMBOL:
    try:
       nam = name+'.csv'
       data_dir = BASE_DIR / 'data' / nam
       data = yf.download(f'{name}.NS',period="max", interval="1d",auto_adjust=True)
       data.to_csv(data_dir)
       df = pd.read_csv(data_dir)
       df=df.drop(index=[0,1])
       df.to_csv(data_dir,index=False)

        
    except Exception as e:
        print (f'{name} --> {e}')



  
  


