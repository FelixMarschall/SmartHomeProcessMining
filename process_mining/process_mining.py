"""
Handels Process Mining Tasks
"""

import pm4py
import pandas as pd 
import numpy as np

class Miner:
    """Event log miner"""
    def __init__(self, file):
        """init"""
        print("Starting miner...")

        # check file
        self.file = file


    def read_file(self, file):
        """Read file"""
        print("Reading file...")

        if file.endswith(".xes"):
            self.file = pm4py.read_xes(file)
        elif file.endswith(".csv"):
            self.file = pm4py.read_ocel_csv(file)
        else:
            print("File format not supported!")
            raise Exception("File format not supported!")