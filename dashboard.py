import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from pathlib import Path
import datetime
import pytz

# Chargement initial des données
def load_data():
    df = pd.read_csv("/home/ubuntu/vix_data.csv", names=["timestamp", "VIX"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
    df = df[df["timestamp"].dt.hour.between(13, 20)]
    return df

# Chargement du rapport quotidien
report_path = Path("/home/ubuntu/daily_report.txt")
if report_path.exists():
    with open(report_path, "r") as file:
        daily_report = file.read()
else:
    daily_report = "No report generated yet."

# Initialisation de Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    # Ticker défilant en haut
    html.Div(id="ticker", style={
        "backgroundColor": "#FFD700",
        "color": "black",
        "padding": "10px",
        "fontWeight": "bold",
        "whiteSpace": "nowrap",
        "overflow": "hidden",
        "textAlign": "center",
        "animation": "scroll-left 20s linear infinite",
        "fontSize": "18px"
    }),

    dcc.Interval(id="time-interval", interval=60*1000, n_intervals=0),
    dcc.Interval(id="update-graph", interval=5*60*1000, n_intervals=0),

    # Heures et switch de thème
    html.Div([
        html.Div(id="paris-ny-time", style={
            "fontSize": "18px",
            "marginBottom": "15px",
            "textAlign": "center",
            "color": "white"
        }),
        html.Div([
            html.Label("Mode :", style={"marginRight": "10px", "color": "white"}),
            dcc.RadioItems(
                id='theme-switch',
                options=[
                    {'label': '🌙 Dark', 'value': 'dark'},
                    {'label': '☀️ Light', 'value': 'light'}
                ],
                value='dark',
                labelStyle={'display': 'inline-block', 'marginRight': '15px'},
                inputStyle={"marginRight": "5px"}
            )
        ], style={"textAlign": "center", "marginBottom": "20px"})
    ]),

    # Sélecteur de granularité
    html.Div([
        html.Label("Vue :", style={"marginRight": "10px", "color": "white"}),
        dcc.RadioItems(
            id='timeframe-selector',
            options=[
                {"label": "📅 Journalier", "value": "daily"},
                {"label": "📈 Hebdomadaire", "value": "weekly"},
                {"label": "📆 Mensuel", "value": "monthly"},
            ],
            value="daily",
            labelStyle={"display": "inline-block", "marginRight": "20px", "color": "white"},
            inputStyle={"marginRight": "5px"}
        )
    ], style={"textAlign": "center", "marginBottom": "20px"}),

    # Graphique et infos du pic
    html.Div([
        html.Div([
            dcc.Graph(id="vix-graph")
        ], style={
            "border": "2px solid #FF6361",
            "borderRadius": "15px",
            "padding": "10px",
            "margin": "10px",
            "boxShadow": "0 0 20px rgba(255,99,97,0.4)"
        }, className="col-md-8"),

        html.Div([
            html.H4("🏆 Pic du jour", style={"textAlign": "center", "color": "#FF6361"}),
            html.Div(id="pic-info", style={
                "backgroundColor": "#121212",
                "padding": "15px",
                "borderRadius": "10px",
                "color": "white",
                "border": "1px solid #FF6361",
                "fontFamily": "monospace"
            })
        ], className="col-md-4")
    ], className="row", style={"margin": "auto", "width": "95%"}),

    # Rapport
    html.H2("📝 Rapport Quotidien (20h)", style={"textAlign": "center", "color": "#FF6361"}),
    html.Pre(daily_report, style={
        "whiteSpace": "pre-wrap",
        "fontFamily": "monospace",
        "backgroundColor": "#121212",
        "padding": "15px",
        "borderRadius": "10px",
        "border": "1px solid #444",
        "color": "white"
    })
], style={"backgroundColor": "#1e1e1e", "padding": "20px", "minHeight": "100vh"})

# Callback : mise à jour du graphique et des infos
@app.callback(
    Output("vix-graph", "figure"),
    Output("pic-info", "children"),
    Input("update-graph", "n_intervals"),
    Input("theme-switch", "value"),
    Input("timeframe-selector", "value")
)
def update_graph(n, theme, timeframe):
    df = load_data()

    if timeframe == "weekly":
        df = df.resample("W-MON", on="timestamp").mean().reset_index()
    elif timeframe == "monthly":
        df = df.resample("M", on="timestamp").mean().reset_index()

    max_point = df.loc[df["VIX"].idxmax()]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["VIX"],
        mode="lines+markers",
        name="VIX",
        line=dict(color="#FF6361"),
        marker=dict(color="red", size=6)
    ))

    fig.add_trace(go.Scatter(
        x=[max_point["timestamp"]],
        y=[max_point["VIX"]],
        mode="markers+text",
        marker=dict(color="gold", size=12, symbol="star"),
        text=["🔥 Pic"],
        textposition="top center",
        showlegend=False
    ))

    bg = "#2e2e2e" if theme == "dark" else "#F9F9F9"
    color = "white" if theme == "dark" else "black"

    fig.update_layout(
        paper_bgcolor=bg,
        plot_bgcolor=bg,
        font=dict(color=color),
        title=f"📊 VIX ({'Jour' if timeframe=='daily' else 'Semaine' if timeframe=='weekly' else 'Mois'})",
        xaxis_title="Date",
        yaxis_title="Indice VIX",
        hovermode="x unified"
    )

    pic_info = f"Max : {max_point['VIX']:.2f}\nDate : {max_point['timestamp'].strftime('%Y-%m-%d')}"

    return fig, pic_info

# Callback : mise à jour du ticker
@app.callback(
    Output("ticker", "children"),
    Input("update-graph", "n_intervals")
)
def update_ticker(n):
    df = load_data()
    last_val = df.iloc[-1]["VIX"]
    max_val = df["VIX"].max()
    min_val = df["VIX"].min()
    return f"🔥 Dernier VIX : {last_val:.2f} | 📈 Max : {max_val:.2f} | 📉 Min : {min_val:.2f} (sur les heures de marché)"

# Callback : mise à jour heure Paris / New York
@app.callback(
    Output("paris-ny-time", "children"),
    Input("time-interval", "n_intervals")
)
def update_times(n):
    paris = datetime.datetime.now(pytz.timezone("Europe/Paris")).strftime("%H:%M:%S")
    ny = datetime.datetime.now(pytz.timezone("America/New_York")).strftime("%H:%M:%S")
    return f"Heure à Paris 🕒 : {paris}  |  Heure à New York 🕒 : {ny}"

# Animation CSS du ticker
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>VIX Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
        @keyframes scroll-left {
            0% {transform: translateX(100%);}
            100% {transform: translateX(-100%);}
        }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)

