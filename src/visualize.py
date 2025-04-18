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


#other imports


#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Global declarations Start Here



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

def visualize_yearly_volume_average(avgYearlyVolume):
    #   TO DO: Exception handler to check if "Output" path exists
    plt.figure(figsize=(10,6))
    plt.plot(avgYearlyVolume['Year'], avgYearlyVolume['Volume'], marker='o', linestyle='-', color='blue')
    plt.title('Average Yearly Bitcoin Trading Volume Per Minute', fontsize='14')
    plt.xlabel('Year', fontsize='12')
    plt.ylabel('Volume Per Minute', fontsize='12')
    plt.xticks(avgYearlyVolume['Year'])
    plt.yticks(np.arange(0,12,step=1))
    plt.grid(True)
    outputPath = Path(__file__).parent.parent / 'Output' / 'YearlyVolumeAvg.png'
    plt.savefig(outputPath, dpi=300, bbox_inches='tight')
#

#%% SELF-RUN               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Code to run when this module is executed directly
    print(f"Running {module_name_gl} module directly")
    visualize()

    # Add any testing or demonstration code here
    visualize_yearly_volume_average(prd.calc_yearly_volume_avg(prd.process_data('Input/btcusd_1-min_data.csv')))
#
