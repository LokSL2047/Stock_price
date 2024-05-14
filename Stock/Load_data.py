# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
import os
import time
from bs4 import BeautifulSoup
import datetime
import matplotlib.dates as mdates

def Web_scrap():
    
    # Specify the URL of the CSV file
    csv_url = "https://query1.finance.yahoo.com/v7/finance/download/0388.HK?period1=1683059431&period2=1714681831&interval=1d&events=history&includeAdjustedClose=true"

    # Specify the desired file name and folder path
    new_file_name = "price_5yrs.csv"
    folder_path = "Data/HK0388/new_data/"

    # Send a GET request to download the file
    response = requests.get(csv_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the file
        new_file_path = os.path.join(folder_path, new_file_name)
        with open(new_file_path, 'wb') as file:
            file.write(response.content)
        print("File downloaded and saved successfully!")
    else:
        print("Failed to download the file. Status code:", response.status_code)
    return


# Read the CSV file into a pandas DataFrame
data = pd.read_csv("Data/HK0388/past_data/price.csv")
Time_label = data.columns[0]


def check_nan_indices(data):
    nan_columns = data.columns[data.isnull().any()]
    
    if len(nan_columns) > 0:
        for column in nan_columns:
            nan_indices = data[column].index[data[column].isnull()]
            print(f"NaN values found in column '{column}' at indices:", nan_indices)
            
def Mean_imputation(data):
    nan_columns = data.columns[data.isnull().any()]
    
    for column in nan_columns:
        mean_value = data[column].mean()
        data[column].fillna(mean_value, inplace=True)
    
    print("Mean imputation done.")


Mean_imputation(data)
check_nan_indices(data)

#Basic analysis
def Basic_plot():
    print("It might take some time...")
    x_axis_label = data.columns[0]
    # Plot the rest of the columns against the first column
    for column in data.columns[1:]:
        # Create a new plot for each column
        plt.figure()
        plt.plot(data[x_axis_label], data[column])
        plt.xlabel(x_axis_label)
        plt.ylabel(column)
        plt.title(f'Plot of {column}')
        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.YearLocator(base=5))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.xticks(rotation=45)
        plt.show()
    return


