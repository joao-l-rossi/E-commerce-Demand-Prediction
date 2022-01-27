import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import plotly.graph_objs as go

st.title("Demand Forecast")
st.markdown("Predicting demand for different products")
st.markdown("Using data from an E-commerce company to predict demand for different types sportwear products in different markets")
st.sidebar.title("Product")
st.sidebar.markdown("Select the product to see forecast:")

df = pd.read_csv("/home/joaolrossi/Desktop/LightHouseLabs/data_bootcamp/Final_Project/Data/df_output_predictions.csv", index_col = "Unnamed: 0")

select_item = st.sidebar.selectbox('Select a product type',list(df.item.unique()))
select_country = st.sidebar.selectbox('Select a product type',list(df.country.unique()))
df_temp = df[(df['item'] == select_item) & (df['country'] == select_country)]


# Create the plotly figure
# Plot code edited from the source below
# https://support.sisense.com/kb/en/article/visualizing-forecasting-data-prophet-in-plotly-%E2%80%94-python

yhat = go.Scatter(
  x = df_temp['ds'],
  y = df_temp['yhat'],
  mode = 'lines',
  marker = {
    'color': '#3bbed7'
  },
  line = {
    'width': 3
  },
  name = 'Forecast',
)

yhat_lower = go.Scatter(
  x = df_temp['ds'],
  y = df_temp['yhat_lower'],
  marker = {
    'color': 'rgba(0,0,0,0)'
  },
  showlegend = False,
  hoverinfo = 'none',
)

yhat_upper = go.Scatter(
  x = df_temp['ds'],
  y = df_temp['yhat_upper'],
  fill='tonexty',
  fillcolor = 'rgba(231, 234, 241,.75)',
  name = 'Confidence',
  hoverinfo = 'none',
  mode = 'none'
)

actual = go.Scatter(
  x = df_temp['ds'],
  y = df_temp["y"],
  mode = 'markers',
  marker = {
    'color': '#fffaef',
    'size': 4,
    'line': {
      'color': '#000000',
      'width': .75
    }
  },
  name = 'Actual'
)

layout = go.Layout(
  yaxis = {
    'title': "Demand for " + select_item + " in " + select_country,
    #'tickformat': format(y_col),
    #'hoverformat': format(y_col)
  },
  hovermode = 'x',
  xaxis = {
    'title': "Days"
  },
  margin = {
    't': 20,
    'b': 50,
    'l': 60,
    'r': 10
  },
  legend = {
    'bgcolor': 'rgba(0,0,0,0)'
  }
)
data = [yhat_lower, yhat_upper, yhat, actual]

fig = dict(data = data, layout = layout)
st.plotly_chart(fig, use_container_width=True)