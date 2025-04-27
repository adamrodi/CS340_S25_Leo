module_name_gl = 'process_data'

'''
Version: v0.1

Description:
    This is the module for processing data. It contains functions and classes
    that help in manipulating and transforming data for further analysis or
    visualization.

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
import numpy as np
import pandas as pd
from itertools import permutations, combinations
from pathlib import Path
import pickle
import config as cfg

#custom imports


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

class VisualizeStats:
    def __init__(self, config=None):
        self.config = config or {}
    #
    
#

class StatsAnalyzer(VisualizeStats):
    def __init__(self):
        super().__init__()
    #

    def joint_counts(self, df, col1, col2):
        return pd.crosstab(df[col1], df[col2])
    #

    def joint_probabilities(self, df, col1, col2):
        counts = self.joint_counts(df, col1, col2)
        return counts / counts.values.sum()
    #

    def conditional_probabilities(self, df, col1, col2):
        return pd.crosstab(df[col1], df[col2], normalize='index')
    #

    def basic_stats(self, df, column):
        return {
            'mean': df[column].mean(),
            'median': df[column].median(),
            'std': df[column].std()
        }
    #

    def vector_ops(self, v1, v2):
        v1 = np.array(v1)
        v2 = np.array(v2)
        return {
            'dot_product': np.dot(v1, v2),
            'angle_deg': np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))),
            'orthogonal': np.isclose(np.dot(v1, v2), 0),
            'unit_v1': v1 / np.linalg.norm(v1),
            'projection_v1_on_v2': np.dot(v1, v2) / np.dot(v2, v2) * v2
        }
    #

    def categorical_analysis(self, df, column):
        values = df[column].unique()
        return {
            'unique': values,
            'permutations': list(permutations(values, 2)),
            'combinations': list(combinations(values, 2))
        }
    #
#


#Function definitions Start Here

#   READ FUNCTIONS
def read_pickle(fileName):
    global outputPath

    if not (outputPath / (fileName + '.pkl')).exists():
        raise FileNotFoundError(f"[read_pickle] File {fileName}.pkl not found in {outputPath}")
    #
    with open((outputPath / (fileName + '.pkl')), 'rb') as file:
        data = pickle.load(file)
    return data
#

def read_csv_data(fileName):
    global inputPath
    if not (inputPath / (fileName + '.csv')).exists():
        raise FileNotFoundError(f"[read_csv_data] File {fileName}.csv not found in {inputPath}")
    #
    with open((inputPath / fileName), "r") as file:
        data = pd.read_csv(file)
        return data
#

#   EXPORT FUNCTIONS
def export_pickle(data, fileName):
    global outputPath
    if (outputPath / (fileName + '.pkl')).exists():
        raise FileExistsError(f"[export_pickle] File {fileName}.pkl already exists in {outputPath}")
    with open((outputPath / (fileName + '.pkl')), "wb") as file:
        pickle.dump(data, file)
#

def export_csv(fileName):
    global outputPath
    try:
        read_pickle(fileName).to_csv((outputPath / (fileName + '.csv')), index=False)
    except Exception as e:
        logger.error(f"[export_csv] Error exporting {fileName}.csv: {e}")
        raise e # propagate the error up the call stack to be handled in main.py
    #
#


#   CALC FUNCTIONS
def calc_yearly_volume_avg(fileName):
    global outputPath
    try:
        data = read_csv_data(fileName)
        data['year'] = pd.to_datetime(data['datetime']).dt.year
        avgYearlyVolume = data.groupby('year')['Volume'].mean().reset_index()
        avgYearlyVolume.columns = ['Year', 'Volume']
        export_pickle(avgYearlyVolume, 'YearlyVolumeAvg')
    except Exception as e:
        raise e # propagate the error up the call stack to be handled in main.py
    #

def calc_local_min_max(file_path, start_date, end_date, chunksize=100_000):
    try:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
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
                max_price = max(max_price, filtered["high"].max())
                min_price = min(min_price, filtered["low"].min())
        return max_price, min_price
    except Exception as e:
        raise e # propagate the error up the call stack to be handled in main.py
#

def calc_percentage_change(file_path, start_date, end_date, price_column="close"):
    try:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        if start >= end:
            raise ValueError("Start date must be earlier than end date.")
        start_value = None
        end_value = None
        for chunk in pd.read_csv(
            file_path,
            usecols=["datetime", price_column],
            parse_dates=["datetime"],
            chunksize=100_000
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
    except Exception as e:
        raise e # propagate the error up the call stack to be handled in main.py
#

def filter_bitcoin_price_by_period(df, period='1y'):
    """
    Filter Bitcoin price data for a specific time period
    
    Parameters:
    -----------
    df : DataFrame
        DataFrame containing Bitcoin price data with 'datetime' column
    period : str
        Time period to filter ('3m', '6m', '1y', '3y', '5y', 'all')
        
    Returns:
    --------
    DataFrame
        Filtered DataFrame with data for the specified period
    """
    # Ensure datetime is in the right format
    if not pd.api.types.is_datetime64_any_dtype(df['datetime']):
        df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Get current date as reference
    end_date = pd.Timestamp.now(tz='UTC')
    
    # Calculate start date based on period
    if period == '3m':
        start_date = end_date - pd.DateOffset(months=3)
    elif period == '6m':
        start_date = end_date - pd.DateOffset(months=6)
    elif period == '1y':
        start_date = end_date - pd.DateOffset(years=1)
    elif period == '3y':
        start_date = end_date - pd.DateOffset(years=3)
    elif period == '5y':
        start_date = end_date - pd.DateOffset(years=5)
    else:  # 'all'
        return df
    
    # Filter the dataframe based on the date range
    filtered_df = df[(df['datetime'] >= start_date) & 
                           (df['datetime'] <= end_date)]
    
    return filtered_df
#

#%% SELF-RUN               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Code to run when this module is executed directly
    print()
    print(f"Running {module_name_gl} module directly")

    # Add any testing or demonstration code here
#
