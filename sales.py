import pandas as pd


class Sales:

    def __init__(self, csv_path):
        self.df = pd.DataFrame(data=csv_path)


