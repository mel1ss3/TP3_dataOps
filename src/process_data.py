import pandas as pd
from typing import List
import os
import glob
from pathlib import Path
import json

col_date: str = "date_heure"
col_donnees: str = "consommation"
cols: List[str] = [col_date, col_donnees]
fic_export_data: str = "data/interim/data.csv"


def load_data():
    list_fic: list[str] = [Path(e) for e in glob.glob("data/raw/*json")]
    list_df: list[pd.DataFrame] = []
    for p in list_fic:
        # list_df.append(pd.read_json(p))
        with open(p, "r") as f:
            dict_data: dict = json.load(f)
            df: pd.DataFrame = pd.DataFrame.from_dict(dict_data.get("results"))
            list_df.append(df)

    df: pd.DataFrame = pd.concat(list_df, ignore_index=True)
    return df


def format_data(df: pd.DataFrame):
    # typage
    df[col_date] = pd.to_datetime(df[col_date])
    # ordre
    df = df.sort_values(col_date)
    # filtrage colonnes
    df = df[cols]
    # dédoublonnage
    df = df.drop_duplicates()
    return df


def export_data(df: pd.DataFrame):
    os.makedirs("data/interim/", exist_ok=True)
    df.to_csv(fic_export_data, index=False)


def main_process():
    df: pd.DataFrame = load_data()
    df = format_data(df)
    df = load_data()
    df = format_data(df)
    
   # Calculer la consommation hebdomadaire
    total = calculate_total(df)
    export_data(df)
    
    # Afficher le total de la consommation hebdomadaire
    calculate_and_display_total(df)

'''
#TODO
    
def calculate_total(df: pd.DataFrame):
# Agréger les données par semaine
    return (df.resample('W-Mon', on=col_date)[col_donnees].sum())
#total = df.resample('W-Mon', on=col_date)[col_donnees].sum()
# return total

'''
    

def calculate_total(df: pd.DataFrame):
    # Agréger les données par semaine et calculer le total de la consommation
    total_consumption = df.resample('W-Mon').sum()
    return total_consumption

def calculate_and_display_total(df: pd.DataFrame):
    total = calculate_total(df)
    print("Consommation totale de la semaine :")
    print(total)


if __name__ == "__main__":

    # data_file: str = "data/raw/eco2mix-regional-tr.csv"
    main_process()
