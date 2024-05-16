import pandas as pd 
from pathlib import Path
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import ticker
import seaborn as sns 
import altair as alt
import plotly.express as px
import plotly.graph_objects as go 
import streamlit as st 


src_file = Path.cwd() / 'vehicles.csv'
img_dir = Path.cwd() / 'images'

df = pd.read_csv(src_file)
df.tail() 

fig = px.histogram(
    df, 
    x = 'comb08',
    color='year',
    labels={'comb08': "Annual Fuel Cost"},
    nbins=40,
    title='Fuel Cost Distribution'
)
fig.show()


st.title('Just Checking...')

st.write(fig)

