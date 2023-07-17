import dash
from django_plotly_dash import DjangoDash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('ventas', external_stylesheets=external_stylesheets)

# carga de datos
df_ventas = pd.read_csv('./panel/data/Ventas.csv',encoding = 'ISO-8859-1',delimiter=',')
# df_ventas_acum = pd.read_csv('./panel/data/Ventas2.csv',encoding = 'ISO-8859-1',delimiter=',')

# definicion de layout
app.layout = html.Div([
                    html.Div([
                    html.Label('País'),
                    dcc.Dropdown(id='selector',
                        options=[{'label': i, 'value': i} for i in df_ventas['PaÃ­s'].unique()],
                        value='Spain'
                    )],style={'width': '48%', 'display': 'inline-block'}),

                   


                    # grafico en blanco
                    html.Div([
                    dcc.Graph(id='barplot_ventas_seg')
                    ],style={'width': '100%', 'float': 'left', 'display': 'inline-block'}),

                   
                   
                    ])

@app.callback(Output('barplot_ventas_seg', 'figure'),
              [Input('selector', 'value')])
def actualizar_graph_seg(seleccion):
    filtered_df = df_ventas[(df_ventas["PaÃ­s"]==seleccion)]

    df_agrupado = filtered_df.groupby("Segmento")["Importe"].agg("sum").to_frame(name = "Ingresos").reset_index()

    return{
        'data': [go.Bar(x=df_agrupado["Segmento"],
                            y=df_agrupado["Ingresos"]
                            )],
        'layout': go.Layout(
            title="¿Cuáles han sido las ventas en cada segmento de clientes?",
            xaxis={'title': "Segmento"},
            yaxis={'title': "Ingresos totales"},
            hovermode='closest'
        )}

