from datetime import date
from dateutil.relativedelta import relativedelta
import yfinance as yf
import os

def load_data_yahoo(symbols, many_month):
    folder_path = "data_csv"  # Replace with the path to your folder
    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Get a list of all files in the folder
        file_list = os.listdir(folder_path)

        # Loop through the files and delete them one by one
        for filename in file_list:
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    #symbols = ['VOO', 'QQQ', 'VGT']

    for symbol in symbols:
        #get last month today - 1 month
        today = date.today().strftime('%Y-%m-%d')
        last_month = date.today() - relativedelta(months=many_month)
        str_last_month = last_month.strftime('%Y-%m-%d')

        # Define the date range
        start_date = str_last_month #data goback in how many month
        #start_date = '2021-03-12' #start from spacific date
        end_date = today
        #end_date = '2021-11-09'#end from spacific date

        # Download historical data
        datacsv = yf.download(symbol, start=start_date, end=end_date)

        # Save the data to a CSV file
        datacsv.to_csv(f"data_csv/{symbol}_usd.csv")