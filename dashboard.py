import pandas as pd
import numpy as np
import plotly.express as px
import warnings as ws
import dash_bootstrap_components as  dbc

from grafico1 import *
from grafico2 import *
from grafico3 import *
from grafico4 import *
from controlador import *
from dash import Dash, html, dash_table
from dash.dependencies import Input, Output

pd.set_option('Display.max_columns', None)
ws.filterwarnings('ignore')


df = pd.read_excel('dados.xlsx', 
                   usecols=['ID_Pedido', 'Data_Pedido', 'ID_Representante',
        'Nome_Representante', 'Regional', 'ID_Produto', 'Nome_Produto',
        'Valor_Produto', 'Quantidade_Vendida', 'Valor_Total_Venda',
        'Nome_Cliente', 'Cidade_Cliente', 'Estado_Cliente'])


external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df_product = html.Div([
    html.H6('Vendas por produto /mês', style={'font-style': 'normal',
                                                'font-weight': '500',
                                                'color': 'black',
                                                'font-style': 'bold',
                                                'letter-spacing': '2px',
                                                'margin-bottom': '10px',
                                                'margin-top': '30px',
                                                'text-align': 'center'}),
    dash_table.DataTable(
        id='df_prod',
        columns=[
            {'name': 'Produto', 'id': 'Nome_Produto'},
            {'name': 'Total de vendas', 'id': 'Valor_Total_Venda'}
        ],
        style_header={'backgroundColor': 'white', 'fontWeight': 'bold', 'text-transform':'uppercase'},
        style_cell={'backgroundColor': 'white', 'color': 'black'}
    )
])

app.layout = dbc.Container(
    children=[
        dbc.Row([
            html.H1('Dashboard de vendas', style = {'text-align': 'center', 
                                                               'font-size': '40px',
                                                               'margin-top': '20px',
                                                               'letter-spacing': '2px',
                                                               }),
            controllers
        ], style={'box-shadow': '0px 4px 6px rgba(255, 255, 255, 0.5)'}),

        dbc.Row([
            grafico1,
    ]),

        dbc.Row([
            dbc.Col([
                grafico2
            ], width=6),
            dbc.Col([
                grafico3
            ], width=6, style = {'margin-top': '20px'})
        ]),

        dbc.Row([
            dbc.Col([grafico4]),
            dbc.Col([df_product], style = {'margin-right': '50px'}),
        ])
    ],
    fluid=True
)


@app.callback([Output('grafico1', 'figure'), Output('grafico2', 'figure'), 
               Output('grafico3', 'figure'), Output('grafico4', 'figure'),
               Output('df_prod', 'data')],
              [Input('monthselection', 'value')])


def update_hist(months):

    df_months = df[df['Data_Pedido'].dt.month == months]
    df_months['day'] = df_months['Data_Pedido'].dt.day
    df_grouped = df_months.groupby('day')['Valor_Total_Venda'].sum().reset_index()
    hist = px.line(df_grouped, x='day', y='Valor_Total_Venda', width=1500,
                      height=600, title='Vendas por mês',
                      color_discrete_sequence= ['green'])
   
    hist.update_layout(
        xaxis_title='Dia do mês',
        yaxis_title='Total de vendas',
        showlegend=False,
        plot_bgcolor='black',
        paper_bgcolor="white",
        font=dict(color='black')
    )

    df_grouped = df_months.groupby('Regional')['Valor_Total_Venda'].sum().reset_index()
    hist2 = px.bar(df_grouped, x='Regional', y='Valor_Total_Venda', width=800,
                      height=600, title='Vendas por região', color = 'Regional',
                      color_discrete_sequence= ['#f7fbff', '#2171b5'])
   
    hist2.update_layout(
        xaxis_title='Região',
        yaxis_title='Total de vendas',
        showlegend=False,
        plot_bgcolor='black',
        paper_bgcolor="white",
        font=dict(color='black')
    )

    pie = px.pie(df_months, names='Nome_Representante', 
                 values='Valor_Total_Venda', width=600, height=600,
                 color_discrete_sequence=px.colors.sequential.Plasma)
   

    pie.update_traces(
        hoverinfo='label+percent',
        textinfo='value',
        textfont=dict(color='black'),
        marker=dict(line=dict(color='white', width=2))
    )

    pie.update_layout(
        showlegend=True,
        legend=dict(font=dict(color='black')),
        plot_bgcolor='black',
        paper_bgcolor="white",
        font=dict(color='black'),
        title=dict(text='Vendas por representante', font=dict(color='black'))
    )



    df_grouped = df_months.groupby('Estado_Cliente')['Valor_Total_Venda'].sum().reset_index().sort_values(by = ['Valor_Total_Venda'])
    hist4 = px.bar(df_grouped, y='Estado_Cliente', x='Valor_Total_Venda', width=800,
                      height=600, title='Vendas por Estado', color = 'Estado_Cliente',
                      color_discrete_sequence= px.colors.sequential.Plasma)
   
    hist4.update_layout(
        xaxis_title='Estado',
        yaxis_title='Total de vendas',
        showlegend=False,
        plot_bgcolor='black',
        paper_bgcolor="white",
        font=dict(color='black')
    )

    df_product = df_months.groupby('Nome_Produto')['Valor_Total_Venda'].sum().reset_index().sort_values(by = ['Valor_Total_Venda'], ascending = False)

    return hist, hist2, pie, hist4, df_product.to_dict('records')
    


if __name__ == '__main__':
    app.run(debug=False)