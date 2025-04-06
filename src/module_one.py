module_name_gl = 'module_one'

'''
Version: v0.1

Description:
    This is the module one for the project. It contains the parent class 1
    and child class 1 as defined in the requirements.

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

class ParentClassOne:
    def __init__(self):
        pass
    #

    def parent_method(self):
        print("This is a method from ParentClassOne.")
    #
#

class ChildClassOne(ParentClassOne):
    def __init__(self):
        super().__init__()
    #

    def child_method(self):
        print("This is a method from ChildClassOne.")
    #
#


#Function definitions Start Here
def module_one():
    pass
#

#%% SELF-RUN               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Code to run when this module is executed directly
    print(f"Running {module_name_gl} module directly")
    module_one()
    # Add any testing or demonstration code here
#
