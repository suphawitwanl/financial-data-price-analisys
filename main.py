import pandas as pd
import os
import matplotlib.pyplot as plt
import dowload_data as get_data_csv

#buy and hold perf not DCA

stock_symbols = ['VOO', 'QQQ', 'VGT', 'SMH', 'SCHG', 'SCHD', 'JEPI']
#stock_symbols = ['BTC-USD']
#stock_symbols = ['VOO', 'QQQ', 'VGT', 'VUG', 'SCHD', 'O', 'XLV', 'XLRE', 'XLF', 'DIA', 'SMH']
#stock_symbols = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'META', 'GOOG', 'BRK-B', 'UNH'] #top10 sp500
#stock_symbols = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'META', 'AVGO', 'TSLA', 'GOOGL', 'GOOG', 'ADBE'] #top10 nasdaq
#stock_symbols = input("Enter symbol to visualize the investment : ").split()
how_many_month_to_goback = 120 #month
get_data_csv.load_data_yahoo(stock_symbols, how_many_month_to_goback)

directory = 'data_csv'
file_names = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
print(file_names)

dir_list = []
for file_n in file_names:
    dir_list.append(f"{directory}/{file_n}")
print(dir_list)

columns = ['avg_perf']
count = 0
for data_name in dir_list:
    data = pd.read_csv(data_name)
    data = data.drop(columns=data.columns[2:7], axis=1)
    first_value = data.iloc[0, 1]
    data['pct_change'] = ((data['Open'] - first_value) / first_value) * 100
    data = data.rename(columns={'pct_change': f'{file_names[count][:-8]}'})
    data = data.drop(columns=['Open'], axis=1)
    columns.append(file_names[count][:-8])
    print(data)

    if count == 0:
        main_df = data[['Date']]
        
    main_df = pd.merge(main_df, data, on='Date', how='outer')
    count += 1


main_df['avg_perf'] = main_df[main_df.columns[1:]].sum(axis=1)/len(file_names)
print(main_df)


# Create a line chart
main_df['Date'] = pd.to_datetime(main_df['Date'])
plt.plot(main_df['Date'], main_df[columns])

# Set the title, labels, and other plot properties
plt.title('Stock Prices')
plt.xlabel('Date')
plt.ylabel('pct_change')
plt.legend(columns)



for cal_comp in columns:
    print()
    # Input values
    perf = round(main_df[cal_comp].iloc[-1], 2)
    beginning_value = 1.0
    ending_value = beginning_value + (perf/100)
    number_of_days = len(main_df)

    days_in_a_year = 365

    # Convert days to years
    number_of_years = number_of_days / days_in_a_year

    # Calculate CAGR
    cagr = (ending_value / beginning_value) ** (1 / number_of_years) - 1

    # Convert CAGR to percentage
    cagr_percentage = cagr * 100

    print(f"The compound annual growth rate (CAGR) of {cal_comp} is: {round(cagr_percentage, 2)}%")
    
print("\n")
plt.show()
