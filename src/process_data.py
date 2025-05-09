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
# Parent class 2
class ConfigStats:

    __DEFAULT_CONFIG = {
        'CLOSE_COLUMN': 'Close',
        'OPEN_COLUMN': 'Open',
        'VOLUME_COLUMN': 'Volume',
        'DATE_COLUMN': 'Date',
        'HIGH_PRICE_THRESHOLD': 50000,
        'LOW_VOLUME_THRESHOLD': 1000000000,
    }

    def __init__(self, config=__DEFAULT_CONFIG):
        self.config = config or {}
    #
    
#
# Child class 2.1
class StatsAnalyzer(ConfigStats):
    def __init__(self):
        super().__init__()
    #

    def load_from_pickle(self, filepath):
        """Load a DataFrame from a pickle file."""
        try:
            self.df = pd.read_pickle(filepath)
            print(f"DataFrame loaded successfully from {filepath}")
        except Exception as e:
            print(f"Failed to load pickle file: {e}")
    #
    def joint_counts(self, df, col1, col2):
        return pd.crosstab(df[col1], df[col2])
    #

    def joint_probabilities(self, df, col1, col2):
        counts = self.joint_counts(df, col1, col2)
        return counts / counts.values.sum()
    #

    def high_price_days(self, threshold=None):
        """Return days where Close > configured threshold."""
        if threshold is None:
            threshold = self.config['HIGH_PRICE_THRESHOLD']
        if self.df is not None:
            return self.df[self.df[self.config['CLOSE_COLUMN']] > threshold]
        else:
            return pd.DataFrame()
    #
    def low_volume_days(self, threshold=None):
        """Return days with Volume below the configured threshold."""
        if threshold is None:
            threshold = self.config['LOW_VOLUME_THRESHOLD']
        if self.df is not None:
            return self.df[self.df[self.config['VOLUME_COLUMN']] < threshold]
        else:
            return pd.DataFrame()
    #

    def visualize_high_price_days(self, threshold=None):
        """Visualize days where Close > configured threshold."""
        if threshold is None:
            threshold = self.config['HIGH_PRICE_THRESHOLD']
        high_price_days = self.high_price_days(threshold)
        if not high_price_days.empty:
            high_price_days.plot(x=self.config['DATE_COLUMN'], y=self.config['CLOSE_COLUMN'])
        else:
            print("No high price days to visualize.")
    #

    def conditional_probabilities(self, df, col1, col2):
        return pd.crosstab(df[col1], df[col2], normalize='index')
    #

    def basic_stats(self, df, *columns):
        results = {}
        for col in columns:
            results[col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std()
            }
        return results
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

    def calc_yearly_volume_avg(fileName):
        global outputPath
        try:
            data = read_csv_data(fileName)
            data['year'] = data['datetime'].apply(lambda x: pd.to_datetime(x).year)
            avgYearlyVolume = data.groupby('year')['Volume'].mean().reset_index()
            avgYearlyVolume.columns = ['Year', 'Volume']
            export_pickle(avgYearlyVolume, 'YearlyVolumeAvg')
        except Exception as e:
            raise e # propagate the error up the call stack to be handled in main.py
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

def prepare_dates(start_date, end_date):
    """Converts start and end dates into pandas Timestamps."""
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    if start >= end:
        raise ValueError("Start date must be earlier than end date.")
    return start, end
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

def array_to_dataframe(array: np.ndarray, column_names=None) -> pd.DataFrame:
    """
    Converts a NumPy mxn array into a pandas DataFrame.
    
    Parameters:
    array : np.ndarray
        The input mxn array.
    column_names : list or None
        Optional list of column names. If None, defaults to integer labels.
    
    Returns:
    pd.DataFrame
        DataFrame constructed from the NumPy array.
    """
    m, n = array.shape
    if column_names is None:
        column_names = [f"Col{i}" for i in range(n)]
    return pd.DataFrame(array, columns=column_names)
#

def evaluate_expression(expr: str):
    try:
        return eval(expr)
    except Exception as e:
        return f"Error: {e}"
#

#%% SELF-RUN               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Code to run when this module is executed directly
    print()
    print(f"Running {module_name_gl} module directly")

    # Add any testing or demonstration code here
#
