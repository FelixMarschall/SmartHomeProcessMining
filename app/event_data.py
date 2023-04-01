import pm4py
import os
PATH_ASSETS = "./app/assets/"

class EventData:
    
    example_log = pm4py.read_xes(PATH_ASSETS + "running-example.xes")
    uploaded_log = None

    # if os.path.isfile(PATH_ASSETS + "temp/uploaded.xes"):
    #     with pm4py.read_xes(PATH_ASSETS + "temp/uploaded.xes") as file:
    #         uploaded_log = file

    

    logbook = None
