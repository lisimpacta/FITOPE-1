import dash
import json
from django_pandas.io import read_frame
from django_plotly_dash import DjangoDash
from core.models import Pagamentos, PedidoOrigem, ClienteOrigem
from django.shortcuts import render
import plotly.graph_objects as go
from pathlib import Path
from plotly.offline import plot
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import pandas as pd
from skimage import io
import plotly.express as px
import numpy as np

cli = ClienteOrigem.objects.all()

app = DjangoDash('dash_integration_financeiro')

ped = PedidoOrigem.objects.all()

df_pedido = read_frame(ped)

cliente = read_frame(cli)

df_pedido_2 = pd.read_csv(str(Path(__file__).parent) + '\\\OPE2.csv')
df_pedido_2['data_pagamento'] = pd.to_datetime(df_pedido_2.data_pagamento)
df_pedido_2.sort_values(by='data_pagamento',inplace=True)
df_pedido_2 = pd.merge(df_pedido_2,cliente,on='cliente_id',how='left')

#print(df_pedido_2['data_pagamento'].astype('datetime64[M]').unique())
df_total = df_pedido_2.set_index(df_pedido_2['data_pagamento'].dt.strftime('%m/%Y')).groupby('categoria')
df_camiseta = df_pedido_2.set_index(df_pedido_2['data_pagamento'].dt.strftime('%m/%Y')).groupby('categoria').get_group('Camiseta').groupby(level=0).sum()
df_bermuda = df_pedido_2.set_index(df_pedido_2['data_pagamento'].dt.strftime('%m/%Y')).groupby('categoria').get_group('Bermuda').groupby(level=0).sum()
df_calca = df_pedido_2.set_index(df_pedido_2['data_pagamento'].dt.strftime('%m/%Y')).groupby('categoria').get_group('Calca').groupby(level=0).sum()
df_camisa = df_pedido_2.set_index(df_pedido_2['data_pagamento'].dt.strftime('%m/%Y')).groupby('categoria').get_group('Camisa').groupby(level=0).sum()
print(df_pedido_2.loc[df_pedido_2['status']=='aguardando pagamento']['valor'].sum())

fig2 = go.Figure()
for i in df_pedido_2.set_index(df_pedido_2['data_pagamento'].astype('datetime64[M]'))['fonte_mkt'].unique():
        fig2.add_trace(go.Scatter(x=df_pedido_2.set_index(df_pedido_2['data_pagamento'].astype('datetime64[M]')).groupby('fonte_mkt').get_group(i).groupby(level=0).sum().index,
         y=df_pedido_2.set_index(df_pedido_2['data_pagamento'].astype('datetime64[M]')).groupby('fonte_mkt').get_group(i).groupby(level=0).sum()['valor'], name=i,
        ))
fig2.update_layout(title='Faturamento mensal por fonte de marketing',plot_bgcolor='white')

fig3 = go.Figure()

fig3.add_trace(go.Indicator(
    value = df_pedido_2.set_index(df_pedido_2['data_pagamento'].astype('datetime64[M]')).groupby(level=0).sum()['2021-02']['valor'][0],
    delta = {'reference': df_pedido_2.set_index(df_pedido_2['data_pagamento'].astype('datetime64[M]')).groupby(level=0).sum()['2021-01']['valor'][0]},
    gauge = {
        'axis': {'visible': False}},
    domain = {'x': [0.0, 0.2], 'y': [0.4, 0.8]}))

fig3.add_trace(go.Indicator(
    mode = "number",
    value = df_pedido_2.loc[df_pedido_2['status']=='aguardando pagamento']['valor'].sum(),
    title = {"text": "Valores<br>aguardando pagamento"},
    domain = {'x': [0.4, 0.6], 'y': [0.4, 0.6]}))

fig3.add_trace(go.Indicator(
    mode = "number",
    value = df_pedido_2.loc[df_pedido_2['status']=='aguardando pagamento']['quantidade'].sum(),
    title = {"text": "Pedidos<br>aguardando pagamento"},
    domain = {'x': [0.7, 1], 'y': [0.4, 0.6]}))

fig3.update_layout(height=250,margin=dict(
            l=50,
            r=30,
            t=0,
            b=0,
        ),
    grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
    template = {'data' : {'indicator': [{
        'title': {'text': "Faturamento x Meta Fev21"},
        'mode' : "number+delta+gauge",
        'delta' : {'reference': 90}}]
                         }})
# fig3.add_trace(go.Indicator(
# mode = "number",
# value = df_pedido_2.groupby(['categoria']).sum()['valor'].max(),
# number = {'prefix': "R$"},
# title = {"text": "Produto com maior faturamento (valor)<br><span style='font-size:0.8em;color:gray'>" +str(mais_faturado) + "</span>"},
# domain = {'x': [0.3, 0.6], 'y': [0, 0.4]}))

# fig3.add_trace(go.Indicator(
# mode = "number",
# value = df_pedido_2.groupby(['fonte_mkt']).sum()['valor'].max(),
# number = {'prefix': "R$"},
# title = {"text": "Melhor fonte de marketing<br><span style='font-size:0.8em;color:gray'>" +str(melhor_mkt) + "</span>"},
# domain = {'x': [0.7, 0.9], 'y': [0, 0.4]}))


app.layout = html.Div([

    html.Div([
                html.Div([
                        dcc.Graph(figure=fig3,id='card1')
                ],style={'width': '100%', 'display': 'inline-block'}),
                    html.Div([
                        html.H3(['Produtos'], style={'margin':'0'}),
                    ],style={'width': '5%', 'display': 'inline-block'}), 
                    html.Div([
                        dcc.Dropdown(
                            id='produto',
                            options=[
                                {'label': 'Camiseta', 'value': 'Camiseta'},
                                {'label': 'Bermuda', 'value': 'Bermuda'},
                                {'label': 'Calça', 'value': 'Calca'},
                                {'label': 'Camisa', 'value': 'Camisa'} 
                                
                            ],
                            value='Camiseta'
                        )
                    ],style={'width': '20%', 'display': 'inline-block'}),

                    html.Div([
                        dcc.Graph(id='grafico')
                ],style={'width': '100%', 'display': 'inline-block'}),
                html.Div([
                        dcc.Graph(figure=fig2,id='grafico-linha')
                ],style={'width': '100%', 'display': 'inline-block'})
                ]),


])

@app.callback(
    dash.dependencies.Output('grafico', 'figure'),
    
    dash.dependencies.Input('produto', 'value'),
    )
def retorna_grafico(val):
    
    ctx = dash.callback_context

    if ctx.triggered==[]:
        prd = 'Camiseta'
    else:

        prd = ctx.triggered[0]["value"]
    print(prd)
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                    shared_yaxes=False, vertical_spacing=0.001)

    fig.append_trace(go.Bar(
        x=df_total.get_group(prd).groupby(level=0).sum()['quantidade'],
        y=df_total.get_group(prd).groupby(level=0).sum().index,
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),
        ),
        name='Quantidade de produtos vendidos',
        orientation='h',
    ), 1, 1)

    fig.append_trace(go.Bar(
        x=df_total.get_group(prd).groupby(level=0).sum()['valor'], y=df_total.get_group(prd).groupby(level=0).sum().index,
        marker=dict(
        color='rgba(255, 200, 52, 0.6)',
            line=dict(
                color='rgba(99, 56, 70, 1.0)',
                width=1),
        ),
        name='Valor vendido',
        orientation='h'
    ), 1, 2)

    fig.update_layout(
        title='Valores e quantidades de ' + prd + ' vendidas',
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0, 0.85],
        ),
        yaxis2=dict(
            showgrid=False,
            showline=True,
            showticklabels=False,
            linecolor='rgba(102, 102, 102, 0.8)',
            linewidth=2,
            domain=[0, 0.85],
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0, 0.42],
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0.47, 1],
            side='top',
            dtick=25000,
        ),
        legend=dict(x=0.029, y=1.038, font_size=10),
        margin=dict(l=100, r=20, t=70, b=70),
        
        plot_bgcolor='white',
    )

    annotations = []

    y_s = np.round(df_total.get_group(prd).groupby(level=0).sum()['quantidade'], decimals=2)
    y_nw = np.rint(df_total.get_group(prd).groupby(level=0).sum()['valor'])


    for ydn, yd, xd in zip(y_nw, y_s, df_total.get_group(prd).groupby(level=0).sum().index):

        annotations.append(dict(xref='x2', yref='y2',
                                y=xd, x=ydn+50,
                                text='R$' + '{:,}'.format(ydn),
                                font=dict(family='Arial', size=12,
                                        color='rgb(128, 0, 128)'),
                                showarrow=False))

        annotations.append(dict(xref='x1', yref='y1',
                                y=xd, x=yd + 2,
                                text=str(yd),
                                font=dict(family='Arial', size=12,
                                        color='rgb(50, 171, 96)'),
                                showarrow=False))

    fig.update_layout(annotations=annotations)
    return fig

# def graficos_financ(request):

#     plot_div = plot({'data': fig}, output_type='div')
#     #plot_div2 = plot({'data': fig2}, output_type='div')
#     return render(request, 'financeiro.html', context={'plot_div': plot_div})
