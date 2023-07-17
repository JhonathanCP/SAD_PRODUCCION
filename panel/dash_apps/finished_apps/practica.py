import dash
import pandas as pd
from django_plotly_dash import DjangoDash
from dash import dcc
from dash import html
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import copy
import psycopg2

# #conexion
# conn=psycopg2.connect(
#     host="localhost",
#     database="datadjango",
#     user="postgres",
#     password="root"
# )

# # crear un objeto cursor
# cur=conn.cursor()

# # ejecutar el query 
# cur.execute("SELECT * FROM crimen_30k")

# results= cur.fetchall()

# df = pd.DataFrame(results, columns=["INCIDENT_NUMBER","OFFENSE_CODE","OFFENSE_CODE_GROUP","OFFENSE_DESCRIPTION","DISTRICT","REPORTING_AREA","SHOOTING","OCCURRED_ON_DATE","YEAR","MONTH","DAY_OF_WEEK","HOUR","UCR_PART","STREET","Lat","Long","Location"])

# print("results")
# print(df)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('practica', external_stylesheets=external_stylesheets)

df = pd.read_csv('./panel/data/crime.csv', encoding='Latin-1',delimiter=',')

# all=df.YEAR.unique()

# # all=df.MONTH.unique()
# print('aqui')

app.layout = html.Div(children = [
    html.H3("Dasboard sobre crímenes en Boston"),
    dcc.Tabs(
        id = 'tabs',
        value = 'estadisticas',
        children = [
            dcc.Tab(
                id = 'estadisticas', 
                value = 'estadisticas',
                label = 'Estadisticas',
                children = [
                    html.Div(
                        id = 'pestanya_estadistica',
                        children = [
                            html.H3("Tab 1"),                            
                            html.Div(id='row1', children=[
                                html.Div(
                                    id = 'div_dropdown',
                                    children = [
                                        dcc.Dropdown(
                                            id = 'iddropdown',
                                            options = [{'label':i, 'value':i} for i in df.UCR_PART.unique()],   
                                            value ='',         
                                            placeholder = 'Añade un valor'
                                        )
                                    ], className = 'three columns'
                                ),
                                 html.Div(
                                        id='divdropdown',
                                        children = [
                                        dcc.Dropdown(
                                            id = 'dropdown_first',
                                            options = [{'label':i, 'value':i} for i in df.YEAR.sort_values().unique()],
                                            # df.YEAR.sort_values().unique()
                                            value ='', 
                                            placeholder = 'Selecciona un año'
                                        )
                                    ], className = 'three columns'
                                    ),
                                html.Div(
                                    id = 'div_dropdown_four',
                                    children = [
                                        dcc.Dropdown(
                                            id = 'iddropdownfour',
                                            options =[{'label':i, 'value':i} for i in df.MONTH.sort_values().unique()],   
                                            value ='',         
                                            placeholder ='Mes'
                                        )
                                    ], className = 'three columns'
                                ),
                                html.Div(
                                    id = 'div_dropdown_three',
                                    children = [
                                        dcc.Dropdown(
                                            id = 'iddropdownthree',
                                            options = [{'label':i, 'value':i} for i in df.DAY_OF_WEEK.unique()],   
                                            value ='',         
                                            placeholder = 'Selecciona un día'
                                        )
                                    ], className = 'three columns'
                                ),
                            ], className = 'row'),                          
                          
                             html.Div([
                                dcc.Graph(id='idbarra')
                                ],style={'width': '50%', 'float': 'left', 'display': 'inline-block'}),

                    html.Div([
                    dcc.Graph(id='idbarratwo')
                    ],style={'width': '50%', 'float': 'center', 'display': 'inline-block'}),

                            
                        ]
                    )
                ]
            ),
            dcc.Tab(
                id = 'datatable',
                value = 'datatable',
                label = 'Tabla de datos',
                children = [
                    html.Div(
                        id = 'pestanya_datatable',
                        children = [
                            html.H3("A continuación mostramos la tabla de datos"),
                           
                        ]
                    )
                ]
            )
        ]
    ),    
])

# callback para componentes

@app.callback(
    Output('iddropdownfour','options'),
    Input('dropdown_first','value'),    
)
def chained_callback_year(year):
    dff=copy.deepcopy(df)
    if year is not None:
        dff=dff.query("YEAR == @year")    
    return sorted(dff["MONTH"].unique())


@app.callback(
    Output('iddropdownthree','options'),
    Input('iddropdownfour','value')    
)
def chined_callback_month(month):
    dff=copy.deepcopy(df)
    if month is not None:
        dff=dff.query("MONTH == @month")    
    return dff["DAY_OF_WEEK"].unique()

@app.callback(
    Output('dropdown_first','options'),
    Input('iddropdown','value')
)
def chined_callback_ucr_year(ucr):
    dff=copy.deepcopy(df)
    if ucr is not None:
        dff=dff.query("UCR_PART == @ucr")
    return sorted(dff["YEAR"].unique())




# Ejemplo 1 - Actualizacion grafico por anyo segun check box
# Ejemplo 2 - Anyadimos dropdown UCR
@app.callback(
    Output('idbarra', 'figure'),
    [Input('iddropdown', 'value'),Input('dropdown_first','value'),Input('iddropdownthree','value'),Input('iddropdownfour','value')]
)

def actualizar_barra(seleccion,selectanio,selectday,selectmonth):
    filtro=df[df["YEAR"]==selectanio]
    filtro_df=df[df["UCR_PART"]==seleccion]
    filtro_day=df[df["DAY_OF_WEEK"]==selectday]   
    filtro_month=df[df["MONTH"]==selectmonth]   
    
    if(len(filtro)==0):
        filtered_df=filtro_df
    else:
        filtered_df=filtro+filtro_df+filtro_day+filtro_month

    
    return{
        'data':[go.Bar(
            x = filtered_df.DISTRICT.value_counts().index.values,
            y = filtered_df.DISTRICT.value_counts().values,
        )],
        'layout':go.Layout(
            title="Total crimenes , año , mes y día",
            xaxis={'title': "UCR"},
            yaxis={'title': "Cantidad de crimenes"}
        )
    }

@app.callback(
    Output('idbarratwo','figure'),
    [Input('iddropdown','value'),Input('dropdown_first','value')]
)
def update_bar(seleccion,selectanio):
    filtro=df[df["YEAR"]==selectanio]
    filtro_df=df[df["UCR_PART"]==seleccion]

    if(len(filtro)==0):
        filtered_df=filtro_df
    else:
        filtered_df=filtro+filtro_df

    
    return{
        'data':[go.Bar(
            x = filtered_df.DISTRICT.value_counts().index.values,
            y = filtered_df.DISTRICT.value_counts().values,
        )],
        'layout':go.Layout(
            title="Total crimen x año",
            xaxis={'title': "UCR"},
            yaxis={'title': "Cantidad de crimenes"}
        )
    }
