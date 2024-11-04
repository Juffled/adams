import csv
import pandas as pd


def csvTimeFormatter(in_path: str, out_path: str):
    
    df = pd.read_csv(in_path)
    
    for i, row in df.iterrows():
        if str(row['Time'])[-1] == "2":
            ifor_val = round(row['Time'] + 0.00005, 5)
        elif str(row['Time'])[-1] == "7":
            ifor_val = round(row['Time'] + 0.00005, 5)
        else:
            ifor_val = round(row['Time'],5)
        df.at[i,'Time'] = ifor_val

    df.to_csv(out_path, index=False)
