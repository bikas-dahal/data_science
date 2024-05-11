from pathlib import Path
import pandas as pd 
from dash import Dash, html, dcc, Input, Output
import plotly.express as px 

app = Dash(__name__)


src_file = Path.cwd() / 'vehicles.csv'
img_dir = Path.cwd() / 'images'

df = pd.read_csv(src_file)


fig = px.histogram(
    df, 
    x = 'comb08',
    color='year',
    labels={'comb08': "Annual Fuel Cost"},
    nbins=40,
    title='Fuel Cost Distribution'
)


app.layout = html.Div(
    children=[
        html.H1('Simple Histogram'),
        html.Div('Annual Fuel Cost Plot'),
        dcc.Graph(
            id='example-histogram', figure=fig
        )
    ]
)


fuel_types = df['fuelType'].unique()


app.layout = html.Div(
    children=[
        html.H1('Simple Histogram'),
        html.Div('Annual Fuel Cost Plot'),
        dcc.Graph(
            id='histogram'
        ),
        dcc.Dropdown(
            id='fuel_id',
            options=[{'label': fuel, 'value': fuel} for fuel in fuel_types],
                value = [fuel for fuel in fuel_types],
                multi=True,  
        )
    ]

)


@app.callback(Output('histogram', 'figure'), Input('fuel_id', 'value'))
def update_output(fuel_list):
    filtered_df = df[df['fuelType'].isin(fuel_list)]
    fig = px.histogram(
        filtered_df, 
        x = 'comb08',
        color='year',
        labels={'comb08': "Annual Fuel Cost"},
        nbins=40,
        title='Fuel Cost Distribution'
    )
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
    
    
