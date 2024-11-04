import csv
import pandas as pd


def csvUnitFormatter(in_path: str, out_path: str, multiplier):

    df = pd.read_csv(in_path)
    list_of_columns = df.columns

    for col in list_of_columns[1:]:
        df[col] = df[col] * multiplier

    df.to_csv(out_path, index=False)
