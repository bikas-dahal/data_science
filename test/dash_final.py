from pathlib import Path
import pandas as pd 
from dash import Dash, html, dcc, Input, Output
import plotly.express as px 
from dash import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {'pre': {'border': 'thin lightgrey solid', 'overflowX':'scroll'}}


src_file = Path.cwd() / 'vehicles.csv'
img_dir = Path.cwd() / 'images'

df = pd.read_csv(src_file)

min_year = int(df['year'].min())
max_year = int(df['year'].max())
all_years = df['year'].unique()
fuelType2_types = df['fuelType2'].unique()

data_table_cols = [
    'make',
    'model',
    'year',
    'fuelType',
    'comb08',
    'city08',
    'displ',
    'cylinders',
    
]


total_clicks = 0

import dash_table
from dash.dash_table.Format import Group

app.layout = html.Div(
    [
        html.H1("Fuel Cost Analysis"),
        html.Div(
            [
                html.P("Talk Python Training Example"),
                dcc.Graph(
                    id="histogram-with-slider",
                    config={"displayModeBar": False},
                ),
                dcc.Graph(id="scatter-plot"),
                html.Label("Year Range"),
                dcc.RangeSlider(
                    id="year-slider",
                    min=min_year,
                    max=max_year,
                    step=1,
                    marks={year: str(year) for year in all_years},
                    value=[min_year, max_year],
                ),
                html.Label("fuelType2 Types"),
                dcc.Checklist(
                    id="fuelType2-type",
                    options=[{"label": i, "value": i} for i in fuelType2_types],
                    value=fuelType2_types,
                    labelStyle={"display": "inline-block"},
                ),
                html.Hr(),
                html.Button("Reset selections", id="reset", n_clicks=0),
                html.H3(id="selected_count"),
                dash_table.DataTable(
                    id="data-table",
                    data=[],
                    columns=[{"name": i, "id": i} for i in data_table_cols],
                    page_size=10,
                    style_table={"height": "300px", "overflowY": "auto"},
                    style_data={"whiteSpace": "normal"},
                ),
            ]
        ),
    ],
    style={"margin-bottom": "150px"},
)

@app.callback(
    Output("histogram-with-slider", "figure"),
    Output("scatter-plot", "figure"),
    Output("data-table", "data"),
    Output("selected_count", "children"),
    Input("year-slider", "value"),
    Input("fuelType2-type", "value"),
    Input("scatter-plot", 'selectedData'),
    Input("reset", "n_clicks"),
)

def update_figure(year_range, fuelType2_list, selectedData, n_clicks):
    # Global Variable may cause unexpected behaviour in multi-user setup
    global total_clicks
    filtered_df = df[df["year"].between(year_range[0], year_range[1])
                     & df['fuelType2'].isin(fuelType2_list)]
    
    fig_hist = px.histogram(
        filtered_df,
        x = 'fuelCost08',
        color='year',
        labels={'fuelCost08': 'Annual Fuel Cost'},
        nbins=40
    )
    
    fig_scatter = px.scatter(
        filtered_df,
        x='comb08',
        y='fuelCost08',
        color='year',
        labels={'comb08': 'Annual Fuel Cost', 'fuelCost08': 'Fuel Cost'},
        hover_data=[filtered_df.index, 'make', 'model', 'year']
    )
    
    fig_scatter.update_layout(clickmode='event', uirevision=True)
    fig_scatter.update_traces(selected_marker_color = 'red')
    
    if n_clicks > total_clicks:
        fig_scatter.update_traces(selected_marker_color = None)
        total_clicks = n_clicks
        selectedData = None
        
        
    if selectedData:
        points = selectedData['points']
        index_list = [
            points[x]['customdata'][0] for x in range(0, len(points))
        ]
        filtered_df = df[df.index.isin(index_list)]
        num_points_label = f'Showing {len(points)} selected points:'
    else:
        num_points_label = 'No points selected - showing top 10 only'
        filtered_df = filtered_df.head(10)
        
    return fig_hist, fig_scatter, filtered_df.to_dict(
        'records'), num_points_label
    
    
    
if __name__ == '__main__':
    app.run_server(debug = True)