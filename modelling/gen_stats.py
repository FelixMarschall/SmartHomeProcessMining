import pandas as pd
import plotly.express as px

def update_day(log: pd.DataFrame):
    """Update the day view."""
    day = px.bar(log, x="time:timestamp", y="costs", color="org:resource", barmode="group")
    return day

def update_week(log: pd.DataFrame):
    """Update the week view."""
    week = px.bar(log, x="time:timestamp", y="costs", color="org:resource", barmode="group")
    return week

def update_month(log: pd.DataFrame):
    """Update the month view."""
    month = px.bar(log, x="time:timestamp", y="costs", color="org:resource", barmode="group")
    return month
