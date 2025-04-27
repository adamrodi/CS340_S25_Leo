module_name_gl = 'visualize'

'''
Version: v0.1

Description:
    This is the module for visualizing data. It contains functions and classes
    that help in creating visual representations of the data processed by
    the application.

Authors:
    Adam Rodi
    Bishow Adhikari
    Caleb Viverito
    Max Del Rio

Date Created     :  4-6-2025
Date Last Updated:  4-7-2025

Doc:
    <***>

Notes:
    <***>
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
   import os
   #os.chdir("./../..")
#
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pathlib import Path

#custom imports
import process_data as prd
import config as cfg


#other imports


#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logger = cfg.get_logger(module_name_gl)

#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Global declarations Start Here
global outputPath
global inputPath

outputPath = Path(__file__).parent.parent / 'Output'
inputPath = Path(__file__).parent.parent / 'Input'


#Class definitions Start Here

class VisualizationHandler:
    """

    """
    def __init__(self, config=None):
        self.config = config or {}
    #

    def visualize_column(self, df, column):
        df[column].plot.line()
        plt.title(f"Line Plot of {column}")
        plt.xlabel(column)
        plt.ylabel("Values")
        plt.grid(True)
        plt.show()
    #

    def simple_query(self, df, column, value):
        return df[df[column] == value]
    #
#

class Plot(VisualizationHandler):
    """
    
    """
    def __init__(self, filepath, config=None):
        super().__init__()
        self.df = pd.read_csv(filepath)
    #

    def plot(self, column_x, column_y=None, method='violin'):
        if method == 'violin':
            sns.violinplot(y=self.df[column_x])
        elif method == 'box':
            sns.boxplot(y=self.df[column_x])
        elif method == 'scatter':
            sns.scatterplot(x=self.df[column_x], y=self.df[column_y])
        plt.title(f"{method.capitalize()} Plot")
        plt.grid(True)
        plt.show()
    #

    def getBoolIndex(self, conditions):
        return self.df.query(conditions)
    #

    

#


#Function definitions Start Here
def visualize():
    pass
#

def visualize_yearly_volume_average(fileName):
    global outputPath

    try: 
        avgYearlyVolume = prd.read_pickle(fileName)
        plt.figure(figsize=(10,6))
        plt.plot(avgYearlyVolume['Year'], avgYearlyVolume['Volume'], marker='o', linestyle='-', color='blue')
        plt.title('Average Yearly Bitcoin Trading Volume Per Minute', fontsize='14')
        plt.xlabel('Year', fontsize='12')
        plt.ylabel('Volume Per Minute', fontsize='12')
        plt.xticks(avgYearlyVolume['Year'])
        plt.yticks(np.arange(0,12,step=1))
        plt.grid(True)
        plt.savefig((outputPath / 'YearlyVolumeAvg.png'), dpi=300, bbox_inches='tight')
    except Exception as e:
        raise e # propagate the error up the call stack to be handled in main.py
#

def visualize_bitcoin_price(data_file, period='1y', save_fig=True):
    """
    Visualize Bitcoin price data for a specific time period
    
    Parameters:
    -----------
    data_file : str
        Name of the CSV file containing Bitcoin price data (without extension)
    period : str
        Time period to visualize ('1m', '3m', '6m', '1y', '3y', '5y', 'all')
    save_fig : bool
        Whether to save the figure to disk
    """
    global inputPath, outputPath
    
    try:
        file_path = inputPath / f"{data_file}.csv"
        bitcoin_data = pd.read_csv(file_path)
        bitcoin_data['datetime'] = pd.to_datetime(bitcoin_data['datetime'])
        filtered_data = prd.filter_bitcoin_price_by_period(bitcoin_data, period)
        filtered_data = filtered_data.dropna(subset=['datetime'])
        if hasattr(filtered_data['datetime'].dt, 'tz'):
            filtered_data = filtered_data.copy()
            filtered_data['datetime'] = filtered_data['datetime'].dt.tz_localize(None)
        #
        plt.figure(figsize=(12, 6))
        plt.plot(filtered_data['datetime'], filtered_data['Close'], 
                 linewidth=1, color='#F7931A')  # Bitcoin orange color
        plt.title(f'Bitcoin Price - {period_to_text(period)}', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price (USD)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        
        if save_fig:
            output_file = outputPath / f'Bitcoin_Price_{period}.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            logger.info(f"Price chart saved to {output_file}")
        #
    #  
    except Exception as e:
        logger.error(f"Failed to visualize Bitcoin price: {e}")
        raise e
#

def period_to_text(period):
    """Convert period code to readable text"""
    period_map = {
        '1m': 'Last 1 Month',
        '3m': 'Last 3 Months',
        '6m': 'Last 6 Months',
        '1y': 'Last 1 Year',
        '3y': 'Last 3 Years',
        '5y': 'Last 5 Years',
        'all': 'All Time'
    }
    return period_map.get(period, period)
#
def find_local_min_max(file_path, start, end, chunksize=100_000):
    """Finds the local maximum and minimum between start and end dates."""
    max_price = None
    min_price = None
    for chunk in pd.read_csv(
        file_path,
        usecols=["datetime", "high", "low"],
        parse_dates=["datetime"],
        chunksize=chunksize
    ):
        filtered = chunk[(chunk["datetime"] >= start) & (chunk["datetime"] <= end)]
        if not filtered.empty:
            max_price = max(max_price, filtered["high"].max()) if max_price is not None else filtered["high"].max()
            min_price = min(min_price, filtered["low"].min()) if min_price is not None else filtered["low"].min()
    return max_price, min_price
#
def find_percentage_change(file_path, start, end, price_column="close", chunksize=100_000):
    """Finds the percentage change of a given price column between start and end dates."""
    start_value = None
    end_value = None
    for chunk in pd.read_csv(
        file_path,
        usecols=["datetime", price_column],
        parse_dates=["datetime"],
        chunksize=chunksize
    ):
        mask = (chunk["datetime"] >= start) & (chunk["datetime"] <= end)
        filtered = chunk.loc[mask]
        if not filtered.empty:
            if start_value is None:
                start_value = filtered.iloc[0][price_column]
            end_value = filtered.iloc[-1][price_column]
    if start_value is None or end_value is None:
        print("No data found in the specified time range.")
        return None
    percentage_change = ((end_value - start_value) / start_value) * 100
    return percentage_change
#

#%% SELF-RUN               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Code to run when this module is executed directly
    print(f"Running {module_name_gl} module directly")
    visualize()

    # Add any testing or demonstration code here
#
