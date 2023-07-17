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
import plotly.express as px


#conexion
conn=psycopg2.connect(
    host="localhost",
    database="datadjango",
    user="postgres",
    password="root"
)

# crear un objeto cursor
cur=conn.cursor()

# ejecutar el query 
cur.execute("SELECT * FROM crimen_30k")

results= cur.fetchall()

df = pd.DataFrame(results, columns=["INCIDENT_NUMBER","OFFENSE_CODE","OFFENSE_CODE_GROUP","OFFENSE_DESCRIPTION","DISTRICT","REPORTING_AREA","SHOOTING","OCCURRED_ON_DATE","YEAR","MONTH","DAY_OF_WEEK","HOUR","UCR_PART","STREET","Lat","Long","Location"])

# print("results")
# print(df)
# print("concatenando")
# tupla=tuple(map(tuple,df[df.YEAR].values.tolist()))
# print(tupla)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('graficothree', external_stylesheets=external_stylesheets)

# df = pd.read_csv('./panel/data/crime.csv', encoding='Latin-1',delimiter=',')

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
                                            options = [{'label':i, 'value':i} for i in df.UCR_PART.dropna().unique()],   
                                            value ='Part One',         
                                            placeholder = 'Añade un valor',                                            
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
                                            # multi=True,                                      
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

# si se requiere que el dropdown aplique sin tener un dropdown anterior| los dropdown anidados se muestren al quitar un dropdown del que dependía quitar el codigo:
#  if year is None:
#         dff=dff.query("YEAR == None")         
# 
# en cada funcion creada

@app.callback(
    [Output('dropdown_first','options')
    ,Output('dropdown_first','value')],
    Input('iddropdown','value')
)
def chined_callback_ucr_year(ucr):
    dff=copy.deepcopy(df)
    if ucr is not None:
        dff=dff.query("UCR_PART == @ucr")
    if ucr is None:
        dff=dff.query("UCR_PART == None")
        
    return sorted(dff["YEAR"].unique()),None



@app.callback(
    [Output('iddropdownfour','options'),
    Output('iddropdownfour', 'value')],
    [Input('dropdown_first','value'),
    Input('iddropdown','value')]
)
def chained_callback_year(year,ucr):
    dff=copy.deepcopy(df)
    if ucr is None:
        dff=dff.query("YEAR == None")        
    if year is not None:
        dff=dff.query("YEAR == @year")
    if year is None:
        dff=dff.query("YEAR == None")             
    return sorted(dff["MONTH"].unique()),None
    # dff=copy.deepcopy(df)
    # if year is not None:
    #     dff=dff.query("YEAR == @year")
    # if year is None:
    #     dff=dff.query("YEAR == None")             

    # return sorted(dff["MONTH"].unique())
    


@app.callback(
    Output('iddropdownthree','options'),
    Output('iddropdownthree','value'),

    [Input('iddropdownfour','value'),
    Input('dropdown_first','value'),
    Input('iddropdown','value')]
    
)
def chined_callback_month(month,year,ucr):
    dff=copy.deepcopy(df)
    if year is None:
        dff=dff.query("MONTH == None") 
    if ucr is None:
        dff=dff.query("MONTH == None") 
    if month is not None:
        dff=dff.query("MONTH == @month")
    if month is None:
        dff=dff.query("MONTH == None") 
    return dff["DAY_OF_WEEK"].unique(),None








# Ejemplo 1 - Actualizacion grafico por anyo segun check box
# Ejemplo 2 - Anyadimos dropdown UCR
@app.callback(
    Output('idbarra', 'figure'),
    [Input('iddropdown', 'value'),Input('dropdown_first','value'),Input('iddropdownthree','value'),Input('iddropdownfour','value')]
)

def actualizar_barra(seleccion,selectanio,selectday,selectmonth):    
    
    filtro_df=df[df["UCR_PART"]==seleccion]
    filtro=df[df["YEAR"]==selectanio]
    # years2=[int(x)for x in selectanio]
    # filtro=df[df.YEAR.isin(years2)]
    filtro_month=df[df["MONTH"]==selectmonth] 
    filtro_day=df[df["DAY_OF_WEEK"]==selectday]     
    filtered_df = df

    
    if len(filtro_df) > 0:
        filtered_df = filtro_df
    if len(filtro) > 0:
        filtered_df = filtered_df.merge(filtro, how='inner')
    if len(filtro_month) > 0:
        filtered_df = filtered_df.merge(filtro_month, how='inner')
    if len(filtro_day) > 0:
        filtered_df = filtered_df.merge(filtro_day, how='inner')


    # if(len(filtro)==0):
    #     filtered_df=filtro_df
                
    # else:
    #     filtered_df = filtro.merge(filtro_df, how='inner')
    #     filtered_df = filtered_df.merge(filtro_month, how='inner')
    #     filtered_df = filtered_df.merge(filtro_day, how='inner')


    
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
    filtro_df=df[df["UCR_PART"]==seleccion]
    filtro=df[df["YEAR"]==selectanio]

    filtered_df = df
    if len(filtro_df) > 0:
        filtered_df = filtro_df
    if len(filtro) > 0:
        filtered_df = filtered_df.merge(filtro, how='inner')


    # if(len(filtro)==0):
    #     filtered_df=filtro_df
        
    # else:        
    #     # how='inner'=> indica una fusion interna(Solo las filas que tienen coincidencias en ambos DataFrames serán incluidas en el resultado)
    #     filtered_df = filtro.merge(filtro_df, how='inner')
        
        
    return{
        'data':[go.Pie(
            labels = filtered_df.DISTRICT.value_counts().index.values,
            values = filtered_df.DISTRICT.value_counts().values,
        )],
        'layout':go.Layout(
            title="Total crimen x año",
            xaxis={'title': "UCR"},
            yaxis={'title': "Cantidad de crimenes"}
        )
    }

