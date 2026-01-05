'''
Updates the data of the stock details in their respective csv files
Fetches the last date on the respective stock(CSV) files and updates them till the current day on which the application is being executed
These changes are then appended in the form of a csv file
'''
import pandas as pd
import yfinance as yf
from datetime import datetime,timedelta


def update_stock_data():

    equity_details = pd.read_csv('C:\\Users\\HP\\OneDrive\\Desktop\\PROJECT\\DATA\\equity_l.CSV')
    
    for name in equity_details.SYMBOL:
        try:
            
             stock_details = pd.read_csv(f'C:\\Users\\HP\\OneDrive\\Desktop\\PROJECT\\DATA\\{name}.CSV')
             dt=stock_details.tail(1).Price.values[0]
             #print(dt)
             today = (datetime.strptime(dt,'%Y-%m-%d')).date()
             next_date=today + timedelta(days=1)
             #start=next_date
             end = (datetime.today().date())
             end1=end + timedelta(days=1)
             #print (today,next_date)
             data=yf.download(f'{name}.NS',start=next_date,end=end1,auto_adjust=True)
             #print (data)
             data.to_csv(f'C:\\Users\\HP\\OneDrive\\Desktop\\PROJECT\\DATA\\{name}.csv',mode='a',header=False)

        except Exception as e:
            print (f'{name} --> {e}')




#update_stock_data()
