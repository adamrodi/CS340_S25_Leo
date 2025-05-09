module_name_gl = 'visualize'

"""
Version        : v0.2
Description    : Visualisation / statistics helpers for the project.
Authors        : Adam Rodi · Bishow Adhikari · Caleb Viverito · Max Del Rio
Date Created   : 2025-04-06
Date Updated   : 2025-05-08
"""

# %% IMPORTS ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    # os.chdir("./../..")
#
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pathlib import Path

# custom imports
import process_data as prd
import config as cfg

# %% CONSTANTS / GLOBALS ──────────────────────────────────────────────────
logger = cfg.get_logger(module_name_gl)

#Global declarations Start Here
global outputPath
global inputPath
outputPath = Path(__file__).parent.parent / 'Output'
inputPath  = Path(__file__).parent.parent / 'Input'

# %% CLASS DEFINITIONS ────────────────────────────────────────────────────
class VisualizationHandler:
    """Base utilities for simple visualisation & querying."""

    def __init__(self, config=None):
        self.config = config or {}

    def visualize_column(self, df, column):
        df[column].plot.line()
        plt.title(f"Line Plot of {column}")
        plt.xlabel(column); 
        plt.ylabel("Values"); 
        plt.grid(True); 
        plt.show()

    def simple_query(self, df, column, value):
        return df[df[column] == value] 


# Parent class 1
class ConfigPlot(VisualizationHandler):
    """Parent-1 : config store, histogram + line helpers, simple query."""

    DEFAULT_CFG = {"figsize": (8, 4), "hist_bins": 20,
                   "line_style": "-", "alpha": 0.75}

    def __init__(self, config=None):
        super().__init__(config or self.DEFAULT_CFG.copy())

    # ---------- visualisations ----------
    def hist_each_column(self, df: pd.DataFrame, save: bool = False, show: bool = False):
        for col in df.select_dtypes(include=np.number):
            plt.figure(figsize=self.config["figsize"])
            df[col].plot.hist(bins=self.config["hist_bins"],
                              alpha=self.config["alpha"], grid=True)
            plt.title(f"Histogram of {col}"); plt.xlabel(col)
            if save:
                fname = outputPath / f"hist_{col}.png"
                plt.savefig(fname, dpi=300, bbox_inches="tight")
                logger.info(f"Saved {fname}")
            if show: plt.show()
            plt.close()
    #
    def line_each_column(self, df: pd.DataFrame, save: bool = False, show: bool = False):
        for col in df.select_dtypes(include=np.number):
            plt.figure(figsize=self.config["figsize"])
            df[col].plot.line(style=self.config["line_style"], grid=True)
            plt.title(f"Line plot of {col}"); plt.ylabel(col)
            if save:
                fname = outputPath / f"line_{col}.png"
                plt.savefig(fname, dpi=300, bbox_inches="tight")
                logger.info(f"Saved {fname}")
            if show: plt.show()
            plt.close()
    #
    # ---------- query ----------
    def query_simple(self, df: pd.DataFrame, column, value):
        return df.loc[df[column] == value]


# Child class 1.1
class DataPlot(ConfigPlot):

    _flag = True

    def __init__(self, filepath: str, config=None):
        super().__init__(config)
        self.df = pd.read_csv(filepath)

    # ---------- visualisations ----------
    def plot(self, x, y=None, *, kind="violin", save=True, show=False):
        plt.figure(figsize=self.config["figsize"])
        if kind == "violin":
            sns.violinplot(y=self.df[x])
        elif kind == "box":
            sns.boxplot(y=self.df[x])
        elif kind == "scatter" and y is not None:
            sns.scatterplot(x=self.df[x], y=self.df[y])
        plt.title(f"{kind.capitalize()} plot of {x}"); plt.grid(True)
        if save:
            suffix = f"{kind}_{x}" if y is None else f"{kind}_{x}_vs_{y}"
            fname = outputPath / f"{suffix}.png"
            plt.savefig(fname, dpi=300, bbox_inches="tight"); logger.info(f"Saved {fname}")
        if show: plt.show()
        plt.close()

    # ---------- boolean query ----------
    def query_bool(self, expression: str):
        return self.df.query(expression)

    def add_numpy_matrix(self, np_array, *col_names, **kwargs):
        if not isinstance(np_array, np.ndarray):
            raise TypeError("np_array must be numpy.ndarray")

        rows, cols = np_array.shape
        if col_names and len(col_names) != cols:
            raise ValueError("Number of column names must match array width.")

        new_df = pd.DataFrame(np_array,
                              columns=list(col_names) or [f"col_{i}" for i in range(cols)],
                              **kwargs)

        # append to existing DataFrame
        def _append():
            nonlocal new_df
            self.df = pd.concat([self.df, new_df], ignore_index=True)
        #
        _append()
        logger.info("NumPy matrix appended.")
        return new_df
    #

    def eval_filter(self, expr: str):
        namespace = {"df": self.df, "np": np, "pd": pd}
        mask = eval(expr, {"__builtins__": {}}, namespace)      # using eval()
        return self.df[mask]

    # ---------- lambda helper ----------
    def lambda_apply(self, column, func=lambda x: x):
        return self.df[column].apply(func)

    # ---------- nonlocal counter demo ----------
    def nonlocal_counter(self):
        cnt = 0
        def inc():
            nonlocal cnt
            cnt += 1
        for _ in range(3): inc()
        return cnt
#

# %% STAND-ALONE FUNCTIONS ────────────────────────────────────────────────
def visualize(): pass

def visualize_yearly_volume_average(fileName):
    try:
        avg = prd.read_pickle(fileName)
        plt.figure(figsize=(10, 6))
        plt.plot(avg['Year'], avg['Volume'], marker='o', linestyle='-', color='blue')
        plt.title('Average Yearly Bitcoin Trading Volume Per Minute')
        plt.xlabel('Year'); plt.ylabel('Volume Per Minute')
        plt.grid(True)
        plt.savefig(outputPath / 'YearlyVolumeAvg.png', dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e: raise e

def visualize_bitcoin_price(data_file, period='1y', save_fig=True):
    try:
        df_path = inputPath / f"{data_file}.csv"
        df = pd.read_csv(df_path)
        df['datetime'] = pd.to_datetime(df['datetime'])
        filtered = prd.filter_bitcoin_price_by_period(df, period).dropna(subset=['datetime'])
        if hasattr(filtered['datetime'].dt, 'tz'):
            filtered['datetime'] = filtered['datetime'].dt.tz_localize(None)

        plt.figure(figsize=(12, 6))
        plt.plot(filtered['datetime'], filtered['Close'], lw=1, color='#F7931A')
        plt.title(f'Bitcoin Price – {period_to_text(period)}')
        plt.xlabel('Date'); plt.ylabel('Price (USD)'); plt.grid(True, alpha=0.3)
        plt.tight_layout()

        if save_fig:
            outfile = outputPath / f'Bitcoin_Price_{period}.png'
            plt.savefig(outfile, dpi=300, bbox_inches='tight')
            logger.info(f"Price chart saved to {outfile}")
        plt.close()
    except Exception as e:
        logger.error(f"Failed to visualise Bitcoin price: {e}")
        raise e

def period_to_text(p):
    return {
            '1m':'Last 1 Month',
            '3m':'Last 3 Months',
            '6m':'Last 6 Months',
            '1y':'Last 1 Year',
            '3y':'Last 3 Years',
            '5y':'Last 5 Years',
            'all':'All Time'
            }.get(p, p)

def find_local_min_max(file_path, start, end, chunksize=100_000):
    max_p = min_p = None
    for ch in pd.read_csv(file_path, usecols=["datetime","high","low"],
                          parse_dates=["datetime"], chunksize=chunksize):
        fil = ch[(ch["datetime"] >= start) & (ch["datetime"] <= end)]
        if not fil.empty:
            max_p = fil["high"].max() if max_p is None else max(max_p, fil["high"].max())
            min_p = fil["low"].min()  if min_p is None else min(min_p, fil["low"].min())
    return max_p, min_p

def find_percentage_change(file_path, start, end, price_column="close", chunksize=100_000):
    start_val = end_val = None
    for ch in pd.read_csv(file_path, usecols=["datetime",price_column],
                          parse_dates=["datetime"], chunksize=chunksize):
        mask = (ch["datetime"] >= start) & (ch["datetime"] <= end)
        fil  = ch.loc[mask]
        if not fil.empty:
            if start_val is None: start_val = fil.iloc[0][price_column]
            end_val = fil.iloc[-1][price_column]
    if start_val is None or end_val is None: return None
    return (end_val - start_val) / start_val * 100

# %% SELF-RUN ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Running {module_name_gl} directly.")

    # quick internal tests
    arr = np.arange(12).reshape(3, 4)
    dp  = DataPlot(inputPath / "btcusd_1-min_data.csv")
    dp.add_numpy_matrix(arr, "A", "B", "C", "D")
    print("nonlocal_counter ->", dp.nonlocal_counter())
