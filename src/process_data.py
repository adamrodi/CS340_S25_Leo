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

#custom imports


#other imports


#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Global declarations Start Here



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
def process_data(filename):
    with open(filename, "r") as csvFile:
        data = pd.read_csv(csvFile)
        return data
#

def calc_yearly_volume_avg(data):
    data['year'] = pd.to_datetime(data['datetime']).dt.year
    avgYearlyVolume = data.groupby('year')['Volume'].mean().reset_index()
    avgYearlyVolume.columns = ['Year', 'Volume']
    return avgYearlyVolume
#

def export_yearly_volume_avg(volumeAvg):
    #   Takes the path the script file is currently in, gets the parent directory (src folder), then gets the parent directory of the src folder (CS340_S25_Leo folder)
    #   then creates a csv file in Output folder.
    #   TO DO:  add exception handler to check if "Output" path exists

    outputPath = Path(__file__).parent.parent / 'Output' / 'YearlyVolumeAvg.csv'
    volumeAvg.to_csv(outputPath, index=False)
#

#%% SELF-RUN               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Code to run when this module is executed directly
    print()
    print(f"Running {module_name_gl} module directly")

    # Add any testing or demonstration code here
    filename = 'Input/btcusd_1-min_data.csv'
    yearlyVolumeAvg = calc_yearly_volume_avg(process_data(filename))
    export_yearly_volume_avg(yearlyVolumeAvg)
#
