import dash
import pandas as pd
from django_plotly_dash import DjangoDash
from dash import dcc
from dash import html
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output,State
import plotly.express as px

# url='https://raw.githubsercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('reportesalud', external_stylesheets=external_stylesheets)
dataset='https://raw.githubusercontent.com/plotly/datasets/master/volcano_db.csv'

df=pd.read_csv(dataset, encoding='Latin-1')

app.layout=html.Div([
    html.Header('Volcano app'),
    dcc.Dropdown(
        id='iddropdown',
        # Type=> parametro de encabezado csv
        options=df["Type"].unique(),
        value='Stratovolcano'
    ),
    dcc.Graph(id='grafico')
])

@app.callback(
    Output('grafico','figure'),
    Input('iddropdown','value')    
)
def sync_input(volcano_selection):
    fig=px.scatter_geo(df.loc[df["Type"]==volcano_selection],
                            lat="Latitude",
                            lon="Longitude",
                            size="Elev"
                            )
    return fig



# df=pd.read_csv('./panel/data/crime_30k.csv', encoding='Latin-1')
# data=df.drop(['Location','Long'],axis=1)

# print('reportesalud - gráfico')
# print(data.head())

# ucr_part unicos(sin repetir)
# ucr_part=data['UCR_PART'].unique()
# diccionario
# options= [{'label':c, 'value':c} for c in ucr_part]

# app.layout=html.Div(
#     [
#         html.H1('Prueba de grafico'),
#         html.Div(            
#             dcc.Dropdown(
#                 id='idDropwdown',
#                 options=options,
#                 value='Part One'
#             ),style={'width':'25%'}
#         ),
#         dcc.Graph(
#             id='grafico',
#             config={'displayModebar':False}
#         )
#     ])

# def update_bar_chart(selected_ucr):
    # filtro_df=data[data['UCR_PART']==selected_ucr]
    # fig=go.Figure(data=[go.Bar(
    #                         name='confirmados',
    #                         x=filtro_df.DISTRICT.value_counts().index.values,
    #                         y=filtro_df.DISTRICT.value_counts().values,
    #                         )])
    # fig.update_layout(title='Numero por distrito')
    # return fig