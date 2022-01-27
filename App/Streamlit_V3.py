import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import plotly.graph_objs as go
from millify import millify

st.set_page_config(layout="wide")
st.title("E-commerce Demand Forecast")
st.markdown("Predicting demand for different products")
st.markdown("This dashboard was designed to contain metrics about E-commerce demand of different types sportswear products in different markets.")


st.sidebar.title("Serie Parameters")
st.sidebar.markdown("Select a product and country to see the forecast:")

df = pd.read_csv("/home/joaolrossi/Desktop/LightHouseLabs/data_bootcamp/Final_Project/Data/df_output_predictions_tuned.csv", index_col = "Unnamed: 0")
df_metrics = pd.read_csv("/home/joaolrossi/Desktop/LightHouseLabs/data_bootcamp/Final_Project/Data/df_metrics_tuned.csv", index_col = "Unnamed: 0")


select_item = st.sidebar.selectbox('Select a product type',list(df.item.unique()))
select_country = st.sidebar.selectbox('Select a country',list(df.country.unique()))
df_temp = df[(df['item'] == select_item) & (df['country'] == select_country)]
df_metrics = df_metrics[(df_metrics['product'] == select_item) & (df_metrics['country'] == select_country)]

st.header('Demand for ' + select_item + " in " + select_country)

# Create the plotly figure
# Plot code edited from the source below
# https://support.sisense.com/kb/en/article/visualizing-forecasting-data-prophet-in-plotly-%E2%80%94-python

yhat = go.Scatter(
  x = df_temp['ds'],
  y = df_temp['yhat'],
  mode = 'lines',
  marker = {
    'color': 'rgba(205, 220, 57,.7)'#'#3bbed7'
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
  fillcolor = 'rgba(158, 158, 158,.7)',
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
  width=10,
  height=400,
  #title='<span style="font-size: 24px;">Demand for ' + select_item + " in " + select_country + '</span>',
  yaxis = {
    'title': '<span style="font-size: 24px;">Units</span>',
    #'tickformat': format(y_col),
    #'hoverformat': format(y_col)
  },
  hovermode = 'x',
  xaxis = {
    'title': '<span style="font-size: 24px;">Days</span>'
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

with st.container():
  st.plotly_chart(fig, use_container_width=True)

with st.container():
  c1, c2, c3, c4 = st.columns(4)
  with c1:
    st.metric(label="Tomorrow", value = millify(df_metrics.tomorrow.values[0],precision=2) , delta = df_metrics.day_increase.values[0])
  with c2:
    st.metric(label="Next Week", value = millify(df_metrics.next_week.values[0],precision=2), delta = df_metrics.week_increase.values[0])
  with c3:
    st.metric(label="Next Month", value = millify(df_metrics.next_month.values[0],precision=2), delta = df_metrics.month_increase.values[0])
  with c4:
    st.metric(label="MAPE", value = millify(df_metrics.mape_best.values[0],precision=2))