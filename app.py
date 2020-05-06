# -*- coding: utf-8 -*-
import dash
import collections
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.read_csv("data.csv", error_bad_lines=False, sep=";")
avgs = (
    df.groupby("model_year")[
        "l/100km",
        "mpg",
        "cylinders",
        "displacement_(cu_in)",
        "displacement_(cc)",
        "horsepower",
        "weight_(lb)",
        "weight_(kg)",
        "acceleration_(0-60mph)",
    ]
    .mean()
    .reset_index()
)
labels = avgs.filter(
    items=[
        "l/100km",
        "mpg",
        "cylinders",
        "displacement_(cu_in)",
        "displacement_(cc)",
        "horsepower",
        "weight_(lb)",
        "weight_(kg)",
        "acceleration_(0-60mph)",
    ]
).columns

prettyLabels = {
    "l/100km": "l/100km",
    "mpg": "mpg",
    "cylinders": "Cylinders",
    "displacement_(cu_in)": "Displacement (cu in)",
    "displacement_(cc)": "Displacement (cc)",
    "horsepower": "Power (BHP)",
    "weight_(lb)": "Weight (lb)",
    "weight_(kg)": "Weight (kg)",
    "acceleration_(0-60mph)": "Acceleration (seconds to 0-60mph)",
}


print(prettyLabels["weight_(kg)"])

app.layout = html.Div(
    [
        dcc.Store(id="session", storage_type="session"),
        dcc.Graph(id="main-graph",),
        html.Div(
            dcc.Slider(
                id="year-slider",
                min=avgs["model_year"].min(),
                max=avgs["model_year"].max(),
                value=avgs["model_year"].min(),
                marks={str(year): str(year) for year in avgs["model_year"].unique()},
                step=None,
                included=False,
                updatemode="drag",
            ),
            style={"width": "100%", "padding": "20px 0px 0px 00px"},
        ),
        html.Div(
            [
                html.Label("X-axis"),
                dcc.Dropdown(
                    id="x-axis",
                    options=[dict(value=x, label=prettyLabels[x]) for x in labels],
                    value=labels[0],
                ),
                html.Label("Y-axis"),
                dcc.Dropdown(
                    id="y-axis",
                    options=[dict(value=x, label=prettyLabels[x]) for x in labels],
                    value=labels[len(labels) - 1],
                ),
            ],
            style={"width": "60%", "margin": "auto"},
        ),
        html.P(
            "Data provided by Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science. Dataset: https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/",
            style={"position": "absolute", "bottom": 0, "left": 0},
        ),
    ]
)


@app.callback(
    Output("main-graph", "figure"),
    [
        Input("session", "data"),
        Input("year-slider", "value"),
        Input("x-axis", "value"),
        Input("y-axis", "value"),
    ],
)
def on_data_set_graph(data, value, x, y):

    return {
        "data": [
            dict(
                x=df.sort_values(by=[x, y]).loc[df["model_year"] == value][x],
                y=df.sort_values(by=[x, y]).loc[df["model_year"] == value][y],
                mode="lines+markers",
                opacity=0.7,
                marker={"size": 10, "color": "blue",},
                name="Values",
                text="(" + x + ", " + y + ")",
            ),
            dict(
                x=avgs.loc[avgs["model_year"] == value][x],
                y=avgs.loc[avgs["model_year"] == value][y],
                name="Average",
                mode="markers",
                opacity=0.7,
                marker={"size": 15, "color": "red",},
                text="(" + x + ", " + y + ")",
            ),
        ],
        "layout": dict(
            xaxis={"title": prettyLabels[x], "range": [df[x].min(), df[x].max()]},
            yaxis={"title": prettyLabels[y], "range": [df[y].min(), df[y].max()]},
            margin={"l": 40, "b": 40, "t": 40, "r": 10},
            legend={"x": 1, "y": 1},
            hovermode="closest",
            title="Car data",
        ),
    }


if __name__ == "__main__":
    app.run_server(debug=True)
