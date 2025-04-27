module_name_gl = 'main'

'''
Version: v0.1

Description:
    This is the main module for the project. It serves as the entry point for
    the program and contains the main function that orchestrates the execution
    of the application.

Authors:
    Adam Rodi
    Bishow Adhikari
    Caleb Viverito
    Max Del Rio

Date Created     :  4-6-2025
Date Last Updated:  4-6-2025

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

#custom imports
import process_data as prd
import visualize as vs
import config as cfg


#other imports


#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logger = cfg.get_logger(module_name_gl)


#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Global declarations Start Here



#Class definitions Start Here



#Function definitions Start Here
def main():
    pass
#

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Main Self-run block
if __name__ == "__main__":
    
    print(f"\"{module_name_gl}\" module begins.")

    #   demo code
    fileName = 'YearlyVolumeAvg'
    bitcoinDataFile = 'btcusd_1-min_data'
    try:
        vs.visualize_bitcoin_price(bitcoinDataFile, period='3m')
        vs.visualize_bitcoin_price(bitcoinDataFile, period='6m')
        prd.calc_percentage_change(bitcoinDataFile)
        vs.visualize_bitcoin_price(bitcoinDataFile, period='1y')
        vs.visualize_bitcoin_price(bitcoinDataFile, period='3y')
        vs.visualize_bitcoin_price(bitcoinDataFile, period='5y')
        vs.visualize_bitcoin_price(bitcoinDataFile, period='all')

        prd.export_csv(fileName)
        vs.visualize_yearly_volume_average(fileName)
    except Exception as e:
        logger.error(e)
        # TO-DO: implement exception handling and logging here
    #
    print(f"\"{module_name_gl}\" module ends.")
#
