
import streamlit as st
import pandas as pd
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, fic_export_data
import logging
import os
import glob

def remove_data(df: pd.DataFrame, last_n_samples: int = 4*3):   
     # df: pd.DataFrame = pd.read_csv(fic_export_data)    
     return df.iloc[:-last_n_samples]    
     # df.to_csv(fic_export_data, index=False)

logging.basicConfig(level=logging.INFO)
 
LAG_N_DAYS: int = 7
 
os.makedirs("data/raw/", exist_ok=True)
os.makedirs("data/interim/", exist_ok=True)
 
for file_path in glob.glob("data/raw/*json"):
    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        logging.warning(e)
 
st.title("Data Visualization App")
 
@st.cache_data(ttl=15 * 60)
def load_data(lag_days: int):
    load_data_from_lag_to_today(lag_days)
    main_process()
    data = pd.read_csv(fic_export_data, parse_dates=[col_date])
    return data
 
df = load_data(LAG_N_DAYS)
df = remove_data(df, last_n_samples=4*24)


st.subheader("Total Consumption for Last Week")
 
# Filter the dataframe to keep only the data for the last week
last_week_start = df[col_date].max() - pd.Timedelta(days=6)
last_week_data = df[df[col_date] >= last_week_start]
 
# Calculate the total consumption for the last week
total_consumption_last_week = last_week_data[col_donnees].sum()
 
st.write(f"Total consumption for last week : {total_consumption_last_week}")
 