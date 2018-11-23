# -*- coding: utf-8 -*

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd

database_file = "../data/database.csv"
df = pd.read_csv(database_file).tail(7)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background' : "black",
    'text' : 'white'
}

def generate_graph_from_data_frame(dataframe, id, title, desired_data_types, series_options, yaxis_title, xaxis_title):
    
    data = []

    for data_type in desired_data_types:
        data.append(go.Scatter(
            {'y' : dataframe[data_type][::-1], 
            'x' : [0, 1, 2, 3, 4, 5, 6], 
            'name' : series_options[data_type]["series_name"],
            'line' : {
                'color' : series_options[data_type]['color']
            }
            },
        ))

    return dcc.Graph(
        id=id,
        figure={
            'data' : data,
            'layout': {
                'title': title,
                'plot_bgcolor' : colors['background'], 
                'paper_bgcolor' : colors['background'],
                'font' : {
                    'color' : colors['text']
                },
                'xaxis' : dict(title=xaxis_title, autorange="reversed"),
                'yaxis' : dict(title=yaxis_title)
            }
        }
    )

def generate_graph_from_raw_data(data, id, title):
    return dcc.Graph(
        id=id, 
        figure={
            'data': data,
            'layout': {
                'title': title,
                'plot_bgcolor' : colors['background'], 
                'paper_bgcolor' : colors['background'],
                'font' : {
                    'color' : colors['text']
                }
            }
        }
    )

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children='STEM Local Atmosphere Monitor (SLAM)', style={
        'textAlign' : 'center', 
        'color' : colors['text']
    }), 

    html.Div(children=[
        html.H2(children="")
        ], style={
        'textAlign' : 'center', 
        'color' : colors['text']
    }),

    generate_graph_from_data_frame(df, "particles", "Methane, CO, and Radon Levels", [
        "CO_levels", "methane_levels", "radon_levels"], 
        {
            "CO_levels" : {
                "series_name" : "Carbon Monoxide Levels",
                "color" : "#fffa00"
            },
            "methane_levels" : {
                "series_name" : "Methane Levels",
                "color" : "#ff8c00"
            },
            "radon_levels" : {
                "series_name" : "Radon Levels",
                "color" : "#ff270f"
            }
        },
        "Concentration (ppm)",
        "Time since last scan (minutes)"
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

