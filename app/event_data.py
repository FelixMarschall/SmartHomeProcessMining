import pm4py

PATH_ASSETS = "./app/assets/"


class EventData:
    example_log = pm4py.read_xes(PATH_ASSETS + "running-example.xes")
    uploaded_log = None
    logbook = None
    logbook_unfiltered = None
