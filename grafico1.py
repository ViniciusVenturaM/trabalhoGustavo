from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout(template = 'plotly_white', paper_bgcolor = 'white')

grafico1 = dbc.Row([
    dcc.Graph(id = 'grafico1', figure = fig) 
],
style={'justify': 'center', 'align': 'center'})