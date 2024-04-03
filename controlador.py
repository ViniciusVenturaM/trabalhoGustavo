import pandas as pd
import warnings as ws
import dash_bootstrap_components as dbc
from  dash import dcc, html

pd.set_option('Display.max_columns', None)
ws.filterwarnings('ignore')


df = pd.read_excel('dados.xlsx', 
                   usecols=['ID_Pedido', 'Data_Pedido', 'ID_Representante',
        'Nome_Representante', 'Regional', 'ID_Produto', 'Nome_Produto',
        'Valor_Produto', 'Quantidade_Vendida', 'Valor_Total_Venda',
        'Nome_Cliente', 'Cidade_Cliente', 'Estado_Cliente'])

months = df['Data_Pedido'].dt.month
months = months.unique()
representatives = df['Nome_Representante'].unique()
products = df['Nome_Produto'].unique()
regions = df['Regional'].unique()
states = df['Estado_Cliente'].unique()

month_dict = {
    'Janeiro': 1,
    'Fevereiro': 2,
    'Março': 3,
    'Abril': 4,
    'Maio': 5,
    'Junho': 6,
    'Julho': 7,
    'Agosto': 8,
    'Setembro': 9,
    'Outubro': 10,
    'Novembro': 11,
    'Dezembro': 12
}



controllers = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H6('Selecione um mês para filtrar', style={'font-style': 'normal',
                                                'font-weight': '500',
                                                'color': 'black',
                                                'letter-spacing': '2px',
                                                'margin-bottom': '5px',
                                                'margin-top': '30px',
                                                'text-align': 'center'}),
            dcc.Dropdown(
                options=[{'label': month, 'value': month_num} for month, month_num in month_dict.items()],
                value=1,
                searchable=False,
                id = 'monthselection',
                style={'color': 'black', 'width': '200px', 'margin': '10px auto 20px auto'}),
        ]),
    ]),
], fluid=True)