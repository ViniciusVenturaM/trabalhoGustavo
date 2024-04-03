from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout(template = 'plotly_white', paper_bgcolor = 'white')

grafico2 = dbc.Row([
    dcc.Graph(id = 'grafico2', figure = fig) 
])