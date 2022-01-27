import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Demand Forecast")
st.markdown("Predicting demand for different products")
st.markdown("Using data from an E-commerce company to predict demand for different types sportwear products in different markets")
st.sidebar.title("Product")
st.sidebar.markdown("Select the product to see forecast:")

df = pd.read_csv("/home/joaolrossi/Desktop/LightHouseLabs/data_bootcamp/Final_Project/Data/df_output_predictions.csv", index_col = "Unnamed: 0")

select_item = st.sidebar.selectbox('Select a product type',list(df.item.unique()))
select_country = st.sidebar.selectbox('Select a product type',list(df.country.unique()))
df_temp = df[(df['item'] == select_item) & (df['country'] == select_country)]
df_observed = df_temp[df_temp["label"] == "Observed"]
df_pred = df_temp[df_temp["label"] == "Predicted"]

df_plot_obs = df_observed["value"]
df_plot_obs.index = df_observed["date"]

df_plot_pred = df_pred["value"]
df_plot_pred.index = df_pred["date"]

st.line_chart(df_plot_obs)
st.line_chart(df_plot_pred)