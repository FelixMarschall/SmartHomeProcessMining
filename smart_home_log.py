import pandas as pd

class SmartHomeLog:
    """Class stores log file as pandas dataframe."""
    _data = pd.read_csv('./example_files/running-example.csv', sep=';')

    @staticmethod
    def set_data(data: pd.DataFrame) -> None:
        """ sets dataframe"""
        SmartHomeLog.data = data

    @staticmethod
    def get_data() -> pd.DataFrame:
        """ returns dataframe"""
        return SmartHomeLog.data