module_name_gl = 'main'

"""
Version: v0.2

Description:
    Entry point for the project.  Shows the menu, handles user choice,
    and then exits (no automatic demo loop).

Authors:
    Adam Rodi
    Bishow Adhikari
    Caleb Viverito
    Max Del Rio
"""

# %% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    import os
    # os.chdir("./../..")
#
import config as cfg
import ui                     # ui drives everything we need

# %% LOGGER                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logger = cfg.get_logger(module_name_gl)

# %% MAIN FUNCTION              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main() -> None:
    ui.displayMenu()
    choice = ui.getChoice()
    ui.displayChoice(choice)

# %% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f'"{module_name_gl}" module begins.')
    main()
    print(f'"{module_name_gl}" module ends.')
