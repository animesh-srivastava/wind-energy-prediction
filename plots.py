import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from exceptions import DatasetNotFoundError
from pickle import load, dump
from cleaning_datasets import Dataset

basedir = os.path.dirname(os.path.abspath(__file__))



if __name__ == '__main__':
    dataset = Dataset()
    print(dataset.df1)

