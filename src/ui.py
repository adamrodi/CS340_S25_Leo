import process_data as prd
import visualize as vs
import config as cfg
from visualize import DataPlot, outputPath 
from pathlib import Path  

module_name_gl = 'ui'
logger = cfg.get_logger(module_name_gl)

# -------------------------------------------------------------------------
def displayMenu():
    print("\n" + "=" * 40)
    print("OPTIONS MENU".center(40))
    print("=" * 40)
    print("1. Visualize BitCoin price by date")
    print("2. Run Test Case 2")
    print("3. Run Test Case 3")
    print("4. Run Test Case 4")
    print("5. Run Test Case 5")
    print("6. Run Test Case 6")
    print("0. Exit")
    print("=" * 40)


def getChoice():
    while True:
        try:
            choice = int(input("\nChoose an option (0-6): "))
            if 0 <= choice <= 6:
                return choice
            print("Please enter a number between 0 and 6")
        except ValueError:
            logger.error(ValueError)
            print("Invalid input. Please enter a number.")


def displayChoice(choice):
    if choice == 1:
        option1()
    elif choice == 2:
        print("Choice 2")
    elif choice == 3:
        print("Choice 3")
    elif choice == 4:
        print("Choice 4")
    elif choice == 5:
        print("Choice 5")
    elif choice == 6:
        print("Choice 6")
    else:
        print("Exit program")

# -------------------------------------------------------------------------
def option1():
    """
    • Ask for a time-period and plot price by date (existing behaviour)
    • THEN offer user to view distribution plots (hist, violin, box, scatter)
    """
    bitcoinDataFile = 'btcusd_1-min_data'           
    input_dir = Path(__file__).parent.parent / 'Input'
    csv_path = input_dir / f"{bitcoinDataFile}.csv"

    print("\n" + "=" * 40)
    print("Visualize BitCoin price by date".center(40))
    print("=" * 40)

    validPeriods = ['3m', '6m', '1y', '3y', '5y', 'all']
    while True:
        periodInput = input("Enter time period\n(3m, 6m, 1y, 3y, 5y, all): ")
        if periodInput in validPeriods:
            try:
                vs.visualize_bitcoin_price(bitcoinDataFile, periodInput)
                break
            except Exception as e:
                logger.error(f"Error visualizing data: {e}")
                print(f"Error: {e} please try again.")
        else:
            print("Invalid period.\n")

    show_more = input("Show column distribution plots? (y/n): ").strip().lower()
    if show_more == 'y':
        try:
            dp = DataPlot(csv_path)

            # Histogram for every numeric column
            dp.hist_each_column(dp.df, save=True)

            # Violin + Box for each numeric column
            num_cols = dp.df.select_dtypes(include='number').columns
            for col in num_cols:
                dp.plot(col, kind='violin', save=True)
                dp.plot(col, kind='box',    save=True)

            # Scatter plot: first two numeric columns, if available
            if len(num_cols) >= 2:
                dp.plot(num_cols[0], y=num_cols[1], kind='scatter', save=True)

            print(f"Saved plots to: {outputPath}")
        except Exception as e:
            logger.error(f"Failed to create distribution plots: {e}")
            print(f"Unable to generate distribution plots ({e}).")
    print("=" * 40)
