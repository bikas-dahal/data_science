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

@st.cache()
def load_data():
    src_file = Path.cwd()  /'vehicles.csv'
    df = pd.read_csv(src_file)
    return df

# load data and determine the valid values 

df = load_data()
min_year = int(df['year'].min())
max_year = int(df['year'].max())
valid_makes = sorted(df['make'].unique())


# Add 'all' as an option to make it easier to select all
valid_makes = ['ALL'] + sorted(df['make'].unique())

# Default make
default_make = df['make'].value_counts().nlargest(5).index.tolist()



st.title('St_2 Example')

make = st.multiselect('Select a make:', valid_makes, default = default_make)
year_range = st.sidebar.slider(
    label= 'Year range',
    min_value= min_year,
    max_value= max_year,
    value=(min_year, max_year),
)



# filter data based on input 

year_filter = df['year'].between(year_range[0], year_range[1])
make_filter = df['make'].isin(make)


plot_df = df[make_filter & year_filter]


# Filter data 
year_filter = df['year'].between(year_range[0], year_range[1])

if 'ALL' in make:
    # Dummy filter to include all makes
    make_filter = True 
else:
    make_filter = df['make'].isin(make)

plot_df = df[make_filter & year_filter]


# st.metric(
#     'Data Frame', plot_df
# )
"""
Calculates the average fuel economy from the 'fuelCost08' column in the `plot_df` DataFrame and displays it as a metric using Streamlit.
"""

avg_fuel_economy = round(plot_df['fuelCost08'].mean(), 0)
st.sidebar.metric(
    'Average', avg_fuel_economy
)


fig = px.histogram(
    plot_df, 
    x = 'comb08',
    color='year',
    labels={'comb08': "Annual Fuel Cost"},
    nbins=40,
    title='Fuel Cost Distribution'
)

altair_chart = (
    alt.Chart(plot_df).mark_tick().encode(
        y = 'fuelType',
        x = 'barrels08'
    )
)

# Display output result 
st.write(fig)
st.write(altair_chart)

st.write('Sample data', plot_df.head(10))