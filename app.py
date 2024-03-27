import streamlit as st
import pandas as pd

# import matplotlib.pyplot as plt
import plotly.express as px
from src.fetch_data import load_data_from_lag_to_today
from src.process_data import col_date, col_donnees, main_process, fic_export_data
import logging
import os
import glob

logging.basicConfig(level=logging.INFO)


LAG_N_DAYS: int = 7

# * INIT REPO FOR DATA
os.makedirs("data/raw/", exist_ok=True)
os.makedirs("data/interim/", exist_ok=True)

# * remove outdated json files
for file_path in glob.glob("data/raw/*json"):
    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        logging.warning(e)

# plt.switch_backend("TkAgg")

# Title for your app
st.title("Data Visualization App")


# Load data from CSV
@st.cache_data(
    ttl=15 * 60
)  # This decorator caches the data to prevent reloading on every interaction.
def load_data(lag_days: int):
    load_data_from_lag_to_today(lag_days)
    main_process()
    data = pd.read_csv(
        fic_export_data, parse_dates=[col_date]
    )  # Adjust 'DateColumn' to your date column name*
    return data


# Assuming your CSV is named 'data.csv' and is in the same directory as your app.py
df = load_data(LAG_N_DAYS)

# Creating a line chart
st.subheader("Line Chart of Numerical Data Over Time")

# Select the numerical column to plot
# This lets the user select a column if there are multiple numerical columns available
# numerical_column = st.selectbox('Select the column to visualize:', df.select_dtypes(include=['float', 'int']).columns)
numerical_column = col_donnees

# ! Matplotlib - Create the plot
# fig, ax = plt.subplots()
# ax.plot(df[col_date], df[numerical_column])  # Adjust 'DateColumn' to your date column name
# ax.set_xlabel('Time')
# ax.set_ylabel(numerical_column)
# ax.set_title(f'Time Series Plot of {numerical_column}')
# # Display the plot
# st.pyplot(fig)

# ! Plotly
# Create interactive line chart using Plotly
fig = px.line(df, x=col_date, y=col_donnees, title="Blablabla")
st.plotly_chart(fig)


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

def calculate_total(df: pd.DataFrame):
    # Agréger les données par semaine et calculer le total de la consommation
    total_consumption = df.resample('W-Mon').sum()
    return total_consumption

def calculate_and_display_total(df: pd.DataFrame):
    total = calculate_total(df)
    print("Consommation totale de la semaine :")
    print(total)

# Définir les fonctions load_data, format_data et export_data ailleurs dans votre code
