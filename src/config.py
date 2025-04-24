module_name_gl = 'config'

'''
Version: v0.1

Description:
    This is the configuration module for the project. It contains constants,
    configurations, and initialization code that are used throughout the
    application.

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

from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

#custom imports


#other imports


#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logDir = Path(__file__).parent.parent / 'Logs'
logFile = logDir / "project.log"

#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Global declarations Start Here



#Class definitions Start Here



#Function definitions Start Here
def config():
    pass
#

def get_logger(name) -> logging.Logger:
    logDir.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)
    file_handler = RotatingFileHandler(
        logDir / f"{name}.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
        )
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter(
            '%(levelname)s: %(message)s'
        )
    )
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger
#

#%% SELF-RUN               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Code to run when this module is executed directly
    print(f"Running {module_name_gl} module directly")
    config()
    # Add any testing or demonstration code here

