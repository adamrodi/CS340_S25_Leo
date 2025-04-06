module_name_gl = 'module_two'

'''
Version: v0.1

Description:
    This is the module two for the project. It contains the parent class 2
    and child class 2 as defined in the requirements.

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


#other imports


#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Global declarations Start Here



#Class definitions Start Here

class ParentClassTwo:
    def __init__(self):
        pass
    #

    def parent_method(self):
        print("This is a method from ParentClassTwo.")
    #
#

class ChildClassTwo(ParentClassTwo):
    def __init__(self):
        super().__init__()
    #

    def child_method(self):
        print("This is a method from ChildClassTwo.")
    #
#


#Function definitions Start Here
def module_two():
    pass
#

#%% SELF-RUN               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Code to run when this module is executed directly
    print(f"Running {module_name_gl} module directly")
    module_two()
    # Add any testing or demonstration code here
#
