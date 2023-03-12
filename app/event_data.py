import pm4py

class EventData:
    example_log = pm4py.read_xes("./app/assets/" + "running-example.xes")
    uploaded_log = None
    logbook = None