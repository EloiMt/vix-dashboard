import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from pathlib import Path
import datetime
print("Chargement CSV...")  # <- ici
df = pd.read_csv("/home/ubuntu/vix_data.csv", names=["timestamp", "VIX"])
df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)

# Filtre les valeurs ou le marché est ouvert.
df = df[df["timestamp"].dt.hour.between(13, 20)]

print("Chargement rapport...")  # <- ici
report_path = Path("/home/ubuntu/daily_report.txt")
if report_path.exists():
    with open(report_path, "r") as file:
        daily_report = file.read()
else:
    daily_report = "No report generated yet."

print("Initialisation de Dash...")  # <- ici
app = dash.Dash(__name__)

# Charger le rapport une seule fois
report_path = Path("/home/ubuntu/daily_report.txt")
if report_path.exists():
    with open(report_path, "r") as file:
        daily_report = file.read()
else:
    daily_report = "No report generated yet."

app.layout = html.Div(children=[
    html.H1(children="📈 VIX Dashboard"),
    
    dcc.Interval(
        id="interval-component",
        interval=5*60*1000,  # toutes les 5 minutes (en millisecondes)
        n_intervals=0
    ),
    
    dcc.Graph(id="vix-graph"),

    html.H2("📝 Rapport Quotidien (20h)"),
    html.Pre(daily_report, style={"whiteSpace": "pre-wrap", "fontFamily": "monospace"})
])


@app.callback(
    Output("vix-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_graph(n):
    df = pd.read_csv("/home/ubuntu/vix_data.csv", names=["timestamp", "VIX"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
    fig = px.line(df, x="timestamp", y="VIX", title="Évolution du VIX")
    return fig


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)

