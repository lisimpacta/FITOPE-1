# coding=iso-8859-1
from datetime import datetime
import dash
import json
from django_pandas.io import read_frame
from django_plotly_dash import DjangoDash
from core.models import Pagamentos, PedidoOrigem, ClienteOrigem
from django.shortcuts import render
import plotly.graph_objects as go
from pathlib import Path
from plotly.offline import plot
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import pandas as pd
from skimage import io
import plotly.express as px

color_scale = px.colors.named_colorscales()
cli = ClienteOrigem.objects.all()

ped = PedidoOrigem.objects.all()

df_pedido = read_frame(ped)

cliente = read_frame(cli)

mapa = open(str(Path(__file__).parent.absolute()) + '\static\imagens\\brasil_estado.json')

brasil = json.load(mapa)

df_pedido_2 = pd.read_csv(str(Path(__file__).parent) + '\\\OPE2.csv')
camiseta = str(Path(__file__).parent.absolute()) + '\static\imagens\camiseta_icon.png'
calca = str(Path(__file__).parent.absolute()) + '\static\imagens\calca_icon.png'
bermuda = str(Path(__file__).parent.absolute()) + '\static'+ '\imagens\\bermuda_icon.png'
camisa = str(Path(__file__).parent.absolute()) + '\static\imagens\camisa_icon.png'

info_cliente = pd.merge(df_pedido_2,cliente,on='cliente_id',how='left')
info_cliente = info_cliente[['estado','valor']].groupby('estado').sum()

brasil_id_map = {}
for feature in brasil['features']:
    feature['id']=feature['properties']["UF_05"]
    brasil_id_map[feature['properties']["NOME_UF"]] = feature['id']

#categoria_quantidade= ped.values('categoria').order_by('categoria').annotate(quantidade = Sum('quantidade'))
df_pedido_2['data_pagamento'] = pd.to_datetime(df_pedido_2.data_pagamento)
df_pedido_2.sort_values(by='data_pagamento',inplace=True)

df3_total=df_pedido_2.loc[(df_pedido_2['categoria']=='Camiseta')]
df3_camiseta = df_pedido_2.loc[(df_pedido_2['data_pagamento']>=pd.to_datetime('2021-01-01')) & (df_pedido_2['data_pagamento']<=pd.to_datetime('2021-04-30')) & (df_pedido_2['categoria']=='Camiseta')]
df3_bermuda = df_pedido_2.loc[(df_pedido_2['data_pagamento']>=pd.to_datetime('2021-01-01')) & (df_pedido_2['data_pagamento']<=pd.to_datetime('2021-04-30')) & (df_pedido_2['categoria']=='Bermuda')]
df3_calca = df_pedido_2.loc[(df_pedido_2['data_pagamento']>=pd.to_datetime('2021-01-01')) & (df_pedido_2['data_pagamento']<=pd.to_datetime('2021-04-30')) & (df_pedido_2['categoria']=='Calca')]
df3_camisa = df_pedido_2.loc[(df_pedido_2['data_pagamento']>=pd.to_datetime('2021-01-01')) & (df_pedido_2['data_pagamento']<=pd.to_datetime('2021-04-30')) & (df_pedido_2['categoria']=='Camisa')]

print(df_pedido_2.set_index(df_pedido_2['data_pagamento']).groupby('categoria').get_group('Camiseta').groupby(level=0).sum().index)
def graficos_vendas(request):

    xvalor_camiseta = df3_camiseta.set_index(df3_camiseta['data_pagamento'].astype('datetime64[W]')).groupby(level=0).sum().index
    xvalor_bermuda = df3_bermuda.set_index(df3_bermuda['data_pagamento'].astype('datetime64[W]')).groupby(level=0).sum().index
    xvalor_calca = df3_calca.set_index(df3_calca['data_pagamento'].astype('datetime64[W]')).groupby(level=0).sum().index
    xvalor_camisa = df3_camisa.set_index(df3_camisa['data_pagamento'].astype('datetime64[W]')).groupby(level=0).sum().index

    # ytotal= df_pedido_2.groupby(['categoria']).get_group('Camiseta')[['valor','data_pagamento']]['valor'].sum()

    yvalor_camiseta = df3_camiseta.set_index(df3_camiseta['data_pagamento'].astype('datetime64[W]')).groupby(level=0).sum()['valor']
    yvalor_bermuda = df3_bermuda.set_index(df3_bermuda['data_pagamento'].astype('datetime64[W]')).groupby(level=0).sum()['valor']
    yvalor_calca = df3_calca.set_index(df3_calca['data_pagamento'].astype('datetime64[W]')).groupby(level=0).sum()['valor']
    yvalor_camisa = df3_camisa.set_index(df3_camisa['data_pagamento'].astype('datetime64[W]')).groupby(level=0).sum()['valor']

    camiseta_mes_ano= df_pedido_2.groupby(['categoria']).get_group('Camiseta')[['valor','data_pagamento']].data_pagamento.dt.to_period("M")
    grupo_camiseta = df_pedido_2.groupby(camiseta_mes_ano).sum()
    bermuda_mes_ano= df_pedido_2.groupby(['categoria']).get_group('Bermuda')[['valor','data_pagamento']].data_pagamento.dt.to_period("M")
    grupo_bermuda = df_pedido_2.groupby(bermuda_mes_ano).sum()
    calca_mes_ano= df_pedido_2.groupby(['categoria']).get_group('Calca')[['valor','data_pagamento']].data_pagamento.dt.to_period("M")
    grupo_calca = df_pedido_2.groupby(calca_mes_ano).sum()
    camisa_mes_ano= df_pedido_2.groupby(['categoria']).get_group('Camisa')[['valor','data_pagamento']].data_pagamento.dt.to_period("M")
    grupo_camisa = df_pedido_2.groupby(camisa_mes_ano).sum()

    mes_ano = df_pedido_2.data_pagamento.dt.to_period("M")
    grupo = df_pedido_2.groupby(mes_ano).sum()
    
    pct_camiseta=pd.merge(grupo_camiseta,grupo,on='data_pagamento',how='left')[['quantidade_x']].div(pd.merge(grupo_camiseta,grupo,on='data_pagamento',how='left')['quantidade_y'],axis=0)
    pct_bermuda=pd.merge(grupo_bermuda,grupo,on='data_pagamento',how='left')[['quantidade_x']].div(pd.merge(grupo_bermuda,grupo,on='data_pagamento',how='left')['quantidade_y'],axis=0)
    pct_calca=pd.merge(grupo_calca,grupo,on='data_pagamento',how='left')[['quantidade_x']].div(pd.merge(grupo_calca,grupo,on='data_pagamento',how='left')['quantidade_y'],axis=0)
    pct_camisa=pd.merge(grupo_camisa,grupo,on='data_pagamento',how='left')[['quantidade_x']].div(pd.merge(grupo_camisa,grupo,on='data_pagamento',how='left')['quantidade_y'],axis=0)

    mais_vendido=df_pedido_2.groupby(['categoria']).sum()['quantidade'].idxmax()
    mais_faturado = df_pedido_2.groupby(['categoria']).sum()['valor'].idxmax()
    melhor_mkt = df_pedido_2.groupby(['fonte_mkt']).sum()['valor'].idxmax()

    night_colors = ['rgb(0, 255, 126)', 'rgb(150, 36, 37)', 'rgb(34, 53, 101)',
                'rgb(99, 236, 57)']

    # fig=go.Figure()
    fig2=fig =px.sunburst(
    df_pedido_2,
    path=['categoria','SKU'],
    values='valor',
    # insidetextorientation='radial'
    )#make_subplots(rows=2,cols=4)
    fig3 = go.Figure()
    fig4 = go.Figure()

    fig4.add_trace(go.Indicator(
    mode = "number",
    value = df_pedido_2.groupby(['categoria']).sum()['quantidade'].max(),
    title = {"text": "Produto mais vendido (unidades)<br><span style='font-size:0.8em;color:gray'>" +str(mais_vendido) + "</span>"},
    domain = {'x': [0.0, 0.2], 'y': [0, 0.4]}))

    fig4.add_trace(go.Indicator(
    mode = "number",
    value = df_pedido_2.groupby(['categoria']).sum()['valor'].max(),
    number = {'prefix': "R$"},
    title = {"text": "Produto com maior faturamento (valor)<br><span style='font-size:0.8em;color:gray'>" +str(mais_faturado) + "</span>"},
    domain = {'x': [0.3, 0.6], 'y': [0, 0.4]}))

    fig4.add_trace(go.Indicator(
    mode = "number",
    value = df_pedido_2.groupby(['fonte_mkt']).sum()['valor'].max(),
    number = {'prefix': "R$"},
    title = {"text": "Melhor fonte de marketing<br><span style='font-size:0.8em;color:gray'>" +str(melhor_mkt) + "</span>"},
    domain = {'x': [0.7, 0.9], 'y': [0, 0.4]}))

    lista_pcts = [pct_camiseta['quantidade_x'].values*100,pct_bermuda['quantidade_x'].values*100,pct_calca['quantidade_x'].values*100,pct_camisa['quantidade_x'].values*100]
    labels = ['Camiseta','Bermuda','Calca','Camisa']

    for i in ['Camiseta','Bermuda','Calca','Camisa']:
        fig3.add_trace(go.Bar(x=df_pedido_2.set_index(df_pedido_2['data_pagamento'].astype('datetime64[M]')).groupby('categoria').get_group(i).groupby(level=0).sum().index,
         y=df_pedido_2.set_index(df_pedido_2['data_pagamento'].astype('datetime64[M]')).groupby('categoria').get_group(i).groupby(level=0).sum()['valor'], name=i
        ))

    # annotations = []
    
    # for y_trace, label, color in zip(lista_pcts, labels, night_colors):

    #     annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
    #                                 xanchor='right', yanchor='middle',
    #                                 text=label + ' {}%'.format(y_trace[0]),
    #                                 font=dict(family='Arial',
    #                                             size=16),
    #                                 showarrow=False))
        

    # annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.0,
    #                             xanchor='left', yanchor='bottom',
    #                             text='Porcentagem Vendas',
    #                             font=dict(family='Arial',
    #                                         size=30,
    #                                         color='rgb(37,37,37)'),
    #                             showarrow=False))

    # fig3.update_layout(annotations=annotations)
    
    fig = px.choropleth(info_cliente, locations=info_cliente.index ,geojson=brasil, color='valor')
    fig.update_geos(fitbounds = "locations", visible = False)

    # fig_line_camiseta = go.Bar(x=xvalor_camiseta,
    # y=yvalor_camiseta, name='Total Camiseta',
    # hovertemplate = 'Valor: %{y:$.2f}<extra></extra>',
    # )

    # fig_line_bermuda = go.Bar(x=xvalor_bermuda,
    # y=yvalor_bermuda, name='Total Bermuda',
    # hovertemplate = 'Valor: %{y:$.2f}<extra></extra>')
    # # marker=dict(color=['rgb(18, 36, 37)']))

    # fig_line_calca = go.Bar(x=xvalor_calca,
    # y=yvalor_calca, name='Total Calça',
    # hovertemplate = 'Valor: %{y:$.2f}<extra></extra>')
    # # marker=dict(color=['rgb(18, 36, 37)']))

    # fig_line_camisa = go.Bar(x=xvalor_camisa,
    # y=yvalor_camisa, name='Total Camisa',
    # hovertemplate = 'Valor: %{y:$.2f}<extra></extra>')
    # # marker=dict(color=['rgb(18, 36, 37)']))

    # fig2.add_trace(go.Image(z=io.imread(camiseta)), row=1,col=1)
    # fig2.add_trace(fig_line_camiseta, row=1,col=2)
    # fig2.add_trace(go.Image(z=io.imread(bermuda)), row=2,col=3)
    # fig2.add_trace(fig_line_bermuda, row=1,col=4)
    # fig2.add_trace(go.Image(z=io.imread(calca)), row=2,col=1)
    # fig2.add_trace(fig_line_calca, row=2,col=2)
    # fig2.add_trace(go.Image(z=io.imread(camisa)), row=1,col=3)
    # fig2.add_trace(fig_line_camisa, row=2,col=4)

    # fig.update_layout(height=500, showlegend=True,
    # paper_bgcolor='rgba(0,0,0,0)',
    # plot_bgcolor='rgba(0,0,0,0)'
    # )
    
    fig2.update_layout(height=500, width=1150, showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis={"visible": False},
    xaxis ={"visible": False},
    yaxis2={"visible": True},
    xaxis2 ={"visible": True},
    yaxis3={"visible": False},
    xaxis3 ={"visible": False},
    yaxis4={"visible": True},
    xaxis4 ={"visible": True},
    yaxis5={"visible": False},
    xaxis5 ={"visible": False},
    yaxis6={"visible": True},
    xaxis6 ={"visible": True},
    yaxis7={"visible": False},
    xaxis7={"visible": False},
    yaxis8={"visible": True},
    xaxis8 ={"visible": True},
    )

    fig3.update_layout(
        barmode='stack',
        # xaxis=dict(
        #     showline=True,
        #     showgrid=False,
        #     showticklabels=True,
        #     linecolor='rgb(204, 204, 204)',
        #     linewidth=2,
        #     ticks='outside',
        #     tickfont=dict(
        #         family='Arial',
        #         size=12,
        #         color='rgb(82, 82, 82)',
        #     ),
        # ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        # autosize=True,
        # margin=dict(
        #     autoexpand=False,
        #     l=100,
        #     r=50,
        #     t=110,
        # ),
        showlegend=True,
        plot_bgcolor='white'
    )

    fig4.update_layout(height=150,
        margin=dict(
            l=50,
            r=30,
            t=0,
            b=1,
        ))

    #fig2 = px.pie(df_pedido, values='valor', names='categoria')
    plot_div = plot({'data': fig}, output_type='div')
    plot_div2 = plot({'data': fig2}, output_type='div')
    plot_div3 = plot({'data': fig3}, output_type='div')
    plot_div4 = plot({'data': fig4}, output_type='div')
    return render(request, 'vendas.html', context={'plot_div': plot_div,'plot_div2':plot_div2,'plot_div3':plot_div3,'plot_div4':plot_div4})
