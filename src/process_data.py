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
    if (outputPath / (fileName + '.csv')).exists():
        raise FileExistsError(f"[export_csv] File {fileName}.csv already exists in {outputPath}")
    try:
        read_pickle(fileName).to_csv((outputPath / (fileName + '.csv')), index=False)
    except Exception as e:
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
def local_max_min():
    pass
#

#%% SELF-RUN               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Code to run when this module is executed directly
    print()
    print(f"Running {module_name_gl} module directly")

    # Add any testing or demonstration code here
#
