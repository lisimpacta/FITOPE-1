import dash
import json
from django_pandas.io import read_frame
from django_plotly_dash import DjangoDash
from core.models import Pagamentos, PedidoOrigem, ClienteOrigem
from django.shortcuts import render
import plotly.graph_objects as go
from pathlib import Path
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import pandas as pd
from skimage import io
import plotly.express as px

global caixa1
global caixa2

app = DjangoDash('dash_integration_id')
cli = ClienteOrigem.objects.all()

ped = PedidoOrigem.objects.all()

df_pedido = read_frame(ped)

cliente = read_frame(cli)

df_pedido_2 = pd.read_csv(str(Path(__file__).parent) + '\\\OPE2.csv')
df_pedido_2['data_pagamento'] = pd.to_datetime(df_pedido_2.data_pagamento)
df_pedido_2.sort_values(by='data_pagamento',inplace=True)
df_pedido_2 = pd.merge(df_pedido_2,cliente,on='cliente_id',how='left')
#info_cliente = info_cliente[['estado','valor']].groupby('estado').sum()

#print(df_pedido_2)
caixa1 = make_subplots(rows=1,cols=2,specs=[[{"type": "bar"}, {"type": "pie"}]])
caixa2 = make_subplots(rows=1,cols=2,specs=[[{"type": "xy"}, {"type": "pie"}]])

caixa1.add_trace(go.Bar(x=['Rotulo 1', 'Rotulo 2'],y=[1,2],name="yaxis"), row=1,col=1)
caixa1.add_trace(go.Pie(labels=['Rotulo 1', 'Rotulo 2'],values=[1,2],name="yaxis"), row=1,col=2)
caixa1.update_layout(height=150, autosize=True,margin=dict(autoexpand=False,
            l=50,
            r=0,
            t=5,
            b=20
        ),
        showlegend=False,
        plot_bgcolor='white')

caixa2.add_trace(go.Scatter(x=['Rotulo 1', 'Rotulo 2','Rotulo3', 'Rotulo 4'],y=[1,4,3,5],name="yaxis"), row=1,col=1)
caixa2.add_trace(go.Pie(labels=['Rotulo 1', 'Rotulo 2'],values=[1,2],name="yaxis",hole=.5), row=1,col=2)
caixa2.update_layout(height=150, autosize=True,margin=dict(autoexpand=False,
            l=50,
            r=0,
            t=5,
            b=30
        ),
        showlegend=False,
        plot_bgcolor='white')


graficos=[]
for i in range(0,4):
    graficos.append(html.Div([

                html.H2(['Gráfico '+str(i+1)]),
                html.Div([
                html.Div([
                    html.Div([
                        html.H3(['Rótulos'], style={'margin':'0'}),
                    ],style={'width': '8%', 'display': 'inline-block'}), 
                    html.Div([
                        dcc.Dropdown(
                            id='rotulo'+str(i+1),
                            options=[
                                {'label': rot, 'value': rot} for rot in df_pedido_2.drop(columns=['nf', 
                                'comments', 'id_pedido', 'cliente_id', 'valor', 'preco_unitario', 'quantidade','email','cep','cidade','bairro','numero','endereco',
                                'cpf','telefone','nome','sobrenome']).columns
                                
                            ],
                        )
                    ],style={'width': '20%', 'display': 'inline-block'}),
                    html.Div([
                        html.H3(['Valores']),
                    ],style={'width': '8%', 'display': 'inline-block'}), 
                    html.Div([
                        dcc.Dropdown(
                            id='valor'+str(i+1),
                            options=[
                                {'label': 'Valor', 'value': 'valor'},
                                {'label': 'Quantidade', 'value': 'quantidade'},
                                {'label': 'Preço Unitário', 'value': 'preco_unitario'}
                            ],
                        )
                    ],style={'width': '20%', 'display': 'inline-block'}),
                ]),

                html.Div([
                    html.Div([
                        dcc.RadioItems(
                                id='seleciona-graf'+str(i+1),
                                options=[
                                    {'label':'Barra', 'value':'barra'},
                                    {'label':'Pizza', 'value':'pizza'},
                                    {'label':'Linha', 'value':'linha'},
                                    {'label':'Donut', 'value':'donut'}],value=[])
                                 
                    ],style={'width': '49%', 'display': 'inline-block'}),
                    # html.Div([
                    #     dcc.RadioItems(
                    #             id='seleciona-graf'+str(i+1),
                    #             options=[
                    #                 {'label':'Pizza', 'value':'pizza'}],value=[])
                    # ],style={'width': '49%', 'display': 'inline-block'})
                ]),

                html.Div([
                        dcc.Graph(figure=caixa1)
                ],style={'width': '100%', 'display': 'inline-block'}, id='out1'+str(i+1)),

                # html.Div([
                #     html.Div([
                #         dcc.RadioItems(
                #                 id='seleciona-graf'+str(i+1),
                #                 options=[
                #                     {'label':'Linha', 'value':'linha'}],value=[]),
                #     ],style={'width': '49%', 'display': 'inline-block'}),
                #     html.Div([
                #         dcc.RadioItems(
                #                 id='seleciona-graf'+str(i+1),
                #                 options=[
                #                     {'label':'Donut', 'value':'donut'}],value=[])
                #     ],style={'width': '49%', 'display': 'inline-block'})
                # ]),
                html.Div([
                        dcc.Graph(figure=caixa2)
                ],style={'width': '100%', 'display': 'inline-block'},id='out2'+str(i+1))
            ])
            ],id='caixa-total'+str(i+1))
            )

app.layout = html.Div([

    html.Div([
        
        graficos[0],
        graficos[1]
    ],style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        graficos[2],
        graficos[3]
    ],style={'width': '49%', 'display': 'inline-block'})
])

@app.callback(
    dash.dependencies.Output('caixa-total1', 'children'),
    
    dash.dependencies.Input('seleciona-graf1', 'value'),
    dash.dependencies.State('rotulo1', 'value'),
    dash.dependencies.State('valor1', 'value'),
    )
def retorna_grafico(sel,rot,val):

    ctx = dash.callback_context
    tipo_grafico = ctx.triggered[0]["value"]
    id_graf = ctx.triggered[0]["prop_id"]
    #print(go.Bar(x=list(df_pedido_2[rot].values),y=list(df_pedido_2[val].values)))
 
    if not ctx.triggered:
        return graficos
        
    if tipo_grafico=='barra':
        return html.Div([
                        dcc.Graph(figure=go.Figure(go.Bar(x=list(df_pedido_2[rot].values),y=list(df_pedido_2[val].values))))
                ], id='caixa-total1')
            
    elif tipo_grafico=='pizza':
        return html.Div([
                dcc.Graph(figure=go.Figure(go.Pie(labels=df_pedido_2[rot],values=df_pedido_2[val])))
        ], id='caixa-total1')
    
    elif tipo_grafico=='linha':
        return  html.Div([
                dcc.Graph(figure=go.Figure(go.Scatter(x=df_pedido_2[rot],y=df_pedido_2[val])))
        ], id='caixa-total1')
    
    elif tipo_grafico=='donut':
        return html.Div([
                        dcc.Graph(figure=go.Figure(go.Pie(labels=df_pedido_2[rot],values=df_pedido_2[val],hole=0.5)))
                ], id='caixa-total1')
            

@app.callback(
    dash.dependencies.Output('caixa-total2', 'children'),
    
    dash.dependencies.Input('seleciona-graf2', 'value'),
    dash.dependencies.State('rotulo2', 'value'),
    dash.dependencies.State('valor2', 'value'),
    )
def retorna_grafico2(sel,rot,val):

    ctx = dash.callback_context
    tipo_grafico = ctx.triggered[0]["value"]
    id_graf = ctx.triggered[0]["prop_id"]
    print(ctx)
    if not ctx.triggered:
        return graficos
    
    if tipo_grafico=='barra':
        return html.Div([
                        dcc.Graph(figure=go.Figure(go.Bar(x=list(df_pedido_2[rot].values),y=list(df_pedido_2[val].values))))
                ], id='caixa-total2')
            
    elif tipo_grafico=='pizza':
        return html.Div([
                dcc.Graph(figure=go.Figure(go.Pie(labels=df_pedido_2[rot],values=df_pedido_2[val])))
        ], id='caixa-total2')
    
    elif tipo_grafico=='linha':
        return  html.Div([
                dcc.Graph(figure=go.Figure(go.Scatter(x=df_pedido_2[rot],y=df_pedido_2[val])))
        ], id='caixa-total2')
    
    elif tipo_grafico=='donut':
        return html.Div([
                        dcc.Graph(figure=go.Figure(go.Pie(labels=df_pedido_2[rot],values=df_pedido_2[val],hole=0.5)))
                ], id='caixa-total2')
            

@app.callback(
    dash.dependencies.Output('caixa-total3', 'children'),
    
    dash.dependencies.Input('seleciona-graf3', 'value'),
    dash.dependencies.State('rotulo3', 'value'),
    dash.dependencies.State('valor3', 'value'),
    )
def retorna_grafico3(sel,rot,val):

    ctx = dash.callback_context
    tipo_grafico = ctx.triggered[0]["value"]
    id_graf = ctx.triggered[0]["prop_id"]
    print(ctx)
    if not ctx.triggered:
        return graficos
    
    if tipo_grafico=='barra':
        return html.Div([
                        dcc.Graph(figure=go.Figure(go.Bar(x=list(df_pedido_2[rot].values),y=list(df_pedido_2[val].values))))
                ], id='caixa-total3')
            
    elif tipo_grafico=='pizza':
        return html.Div([
                dcc.Graph(figure=go.Figure(go.Pie(labels=df_pedido_2[rot],values=df_pedido_2[val])))
        ], id='caixa-total3')
    
    elif tipo_grafico=='linha':
        return  html.Div([
                dcc.Graph(figure=go.Figure(go.Scatter(x=df_pedido_2[rot],y=df_pedido_2[val])))
        ], id='caixa-total3')
    
    elif tipo_grafico=='donut':
        return html.Div([
                        dcc.Graph(figure=go.Figure(go.Pie(labels=df_pedido_2[rot],values=df_pedido_2[val],hole=0.5)))
                ], id='caixa-total3')
            

@app.callback(
    dash.dependencies.Output('caixa-total4', 'children'),
    
    dash.dependencies.Input('seleciona-graf4', 'value'),
    dash.dependencies.State('rotulo4', 'value'),
    dash.dependencies.State('valor4', 'value'),
    )
def retorna_grafico4(sel,rot,val):

    ctx = dash.callback_context
    tipo_grafico = ctx.triggered[0]["value"]
    id_graf = ctx.triggered[0]["prop_id"]
    print(ctx)
    if not ctx.triggered:
        return graficos

    if tipo_grafico=='barra':
        return html.Div([
                        dcc.Graph(figure=go.Figure(go.Bar(x=list(df_pedido_2[rot].values),y=list(df_pedido_2[val].values))))
                ], id='caixa-total4')
            
    elif tipo_grafico=='pizza':
        return html.Div([
                dcc.Graph(figure=go.Figure(go.Pie(labels=df_pedido_2[rot],values=df_pedido_2[val])))
        ], id='caixa-total4')
    
    elif tipo_grafico=='linha':
        return  html.Div([
                dcc.Graph(figure=go.Figure(go.Scatter(x=df_pedido_2[rot],y=df_pedido_2[val])))
        ], id='caixa-total4')
    
    elif tipo_grafico=='donut':
        return html.Div([
                        dcc.Graph(figure=go.Figure(go.Pie(labels=df_pedido_2[rot],values=df_pedido_2[val],hole=0.5)))
                ], id='caixa-total4')
            

