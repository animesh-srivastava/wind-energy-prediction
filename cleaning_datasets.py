import pandas as pd
import os
from pickle import load as load_pickle, dump as dump_pickle
from exceptions import DatasetNotFoundError

basedir = os.path.dirname(os.path.abspath(__file__))

class Dataset(object):
    def __init__(self):
        self.df1 = self._load_from_pickle("df1.pickle")
        self.df2 = self._load_from_pickle("df2.pickle")


    def _read_dataset(self, path_to_dataset: str):
        """
        This function reads the dataset and returns the dataframe
        """
        if not os.path.isabs(path_to_dataset):
            path_to_dataset = os.path.join(basedir, path_to_dataset)
        if os.path.isfile(path_to_dataset):
            return pd.read_csv(path_to_dataset)
        raise DatasetNotFoundError("Dataset not found: {}".format(path_to_dataset))

    def _save_to_pickle(self, filename, df):
        """
        This function saves the pandas dataframe to pickle file
        """
        with open(os.path.join(basedir, "dataset", filename), "wb") as f:
            dump_pickle(df, f)

    def _load_from_pickle(self, filename):
        """
        This function reads the variable from the given pickle file
        """
        if os.path.isfile(os.path.join(basedir, "dataset", filename)):
            with open(os.path.join(basedir, "dataset", filename), "rb") as f:
                return load_pickle(f)
        raise DatasetNotFoundError("Dataset not found {}".format(os.path.join(basedir, "dataset", filename)))



def get_hourly_data_from_df(df: pd.DataFrame):
    hourly_data = [pd.DataFrame()]*(df.shape[0]//10957)
    starts = range(0, df.shape[0], 24)
    for i, start in enumerate(starts):
        if i == 0:
            continue
        print("\r", i, end="")
        for j in range(starts[i-1], start):
            hourly_data[j%24] = \
                hourly_data[j%24].append(df.iloc[j, :])

def get_yearly_data_from_df(df: pd.DataFrame) -> list:
    yearly_data = []
    starts = range(0, df.shape[0], 365)
    for i, start in enumerate(starts):
        if i == 0:
            continue
        yearly_data.append(df.iloc[starts[i-1]:start, :])
    return yearly_data


def saving_dissected_datasets(hourly_data: list):
    for i, df in enumerate(hourly_data):
        yearly_data = get_yearly_data_from_df(df)
        for j, year in enumerate(yearly_data):
            with open(
                "dataset/complete_dataset/hour-{}-year-{}.pickle"
                    .format(i, j), "wb") as f:
                dump_pickle(year, f)

def loading_dissected_datasets(year: int, hour: int) -> pd.DataFrame:
    """
    Loads dataset for provided year and hour
    """
    assert year >= 0 and year < 30, "Year should be between 0 and 29"
    assert hour >= 0 and hour < 24, "Hour should be between 0 and 23"
    with open("dataset/complete_dataset/hour-{}-year-{}.pickle"
        .format(hour, year), "rb") as f:
        return load_pickle(f)

if __name__ == '__main__':
    pass