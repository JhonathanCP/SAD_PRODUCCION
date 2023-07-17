import dash
from dash import dcc
from dash import html
from django_plotly_dash import DjangoDash
import numpy as np
from datetime import datetime as dt
import plotly.graph_objects as go

# creando la aplicación, pasar nombre y los estilos(external_stylesheets)

external_stylesheets = ['https:codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('graficotwo', external_stylesheets=external_stylesheets)

# creacion de layout
app.layout = html.Div([
    html.H1("Hello world"),
    dcc.Graph(
        id='mi_first_graph',
        figure={
            # pasar la data desde la BD
           'data': [
               {'x': [1, 2, 3], 'y':[23, 15, 22],
                   'type':'line', 'name':'vista'},
               {'x': [1, 2, 3], 'y':[5, 2, 8], 'type':'bar', 'name':'click'}
           ],
            # diseño
            'layout':{
                'title': 'Mi gráfico con Dash'
           }
        }
    ),
    html.H1("Componentes"),
    html.Div([
        html.H3('Dropdown'),
        dcc.Dropdown(
            id='dropdown-component',
            options=[
                {'label': 'Big Data', 'value': 'bigdata'},
                {'label': 'Data Science', 'value': 'datascience'},
                {'label': 'Bases de Datos', 'value': 'database'},
                {'label': 'Web', 'value': 'web'}
            ],
            placeholder="Seleeciona una categoria",
            multi=True,
            searchable=True,
            value='bigdata',
            disabled=False,
            className='six columns'
        )
    ], className="row"),
    html.Div([
        html.H3("Slider"),
        dcc.Slider(
            id='slider-component',
            min=0,
            max=100,
            step=5,
            value=0,
            updatemode='mouseup',
            marks={int(i): f'{i}%' for i in np.arange(0, 101, 5)},
            className='nine columns'
        )
    ], className="row", style={'padding-top': '100px'}),
    html.Div(id='textarea-checkbox-radioitems',
             children=[
                 html.H3('Text-area'),
                 dcc.Textarea(
                     id='textarea',
                     placeholder='Escribe aqui tu texto',
                     value='',
                     cols=50,
                     rows=10,
                     autoFocus='True',
                     disabled=False
                 ),
                 html.H3('Check List'),
                 dcc.Checklist(
                     id='checklist',
                     options=[
                         {'label': 'Big data', 'value': 'bigdata'},
                         {'label': 'Data Science',
                             'value': 'datascience', 'disabled': 'False'},
                         {'label': 'Base de Datos', 'value': 'database'},
                         {'label': 'Web', 'value': 'web'}
                     ],
                     value=['bigdata', 'database'],
                     labelStyle={'display': 'inline-block'}
                 )
             ], className="row", style={'padding-top': '100px'}
             ),
    html.H3('Select radio'),
    dcc.RadioItems(
        id='radioitems',
        options=[
            {'label': 'Big data', 'value': 'bigdata'},
            {'label': 'Data Science', 'value': 'datascience'},
            {'label': 'Base de Datos', 'value': 'database'},
            {'label': 'Web', 'value': 'web'}
        ], className='row'),
    html.Div(id='button-dates-markdown', children=[
        html.H3('Boton'),
        html.Button(
            'Enviar',
            id='button',
            contentEditable='False',
            hidden=False,
            n_clicks=0,
            n_clicks_timestamp=-1
        ),
        dcc.Markdown(
            id='markdown',
            children='''
                    ### Markdown
                    Este es un texto en **markdown**, el cual es *interpretado*
                    '''

        )
    ]),
    html.H3('Upload'),
    html.Div(id='upload-tabs-graph', children=[
        dcc.Upload(
                id='upload-data',
                children=[
                    'Arrastra tus ficheros o', html.A('Selecciona')
                ],
            multiple=True,
            min_size=-1,
            max_size=1024,
            style={
                    'width': '50%',
                    'height': '60px',
                    'LineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dash',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
            }
        )
    ]),
    html.Div(children=[
        dcc.Tabs(id='tabs', value='graficotwo', children=[
            dcc.Tab(
                    id='tabone',
                    value='graficoone',
                    label='Gráfico 1',
                    children=[
                        dcc.Graph(
                        id='mi_first_graph',
                        figure={
                            # pasar la data desde la BD
                            'data': [
                                {'x': [1, 2, 3], 'y':[23, 15, 22],
                                 'type':'line', 'name':'vista'},
                                {'x': [1, 2, 3], 'y':[5, 2, 8],
                                 'type':'bar', 'name':'click'}
                            ],
                            # diseño
                            'layout':{
                                'title': 'Mi gráfico con Dash'
                            }
                        }
                    ),
                    ]
            ),
            dcc.Tab(
                id='tabtwo',
                value='graficotwo',
                label='Gráfico 2',
                children=[
                    dcc.Graph(
                        id='mi_second_graph',
                        figure={
                            # pasar la data desde la BD
                            'data': [
                                {'x': [1, 2, 3], 'y':[5, 3, 9],
                                 'type':'line', 'name':'vista'},
                                {'x': [1, 2, 3], 'y':[10, 6, 13],
                                 'type':'bar', 'name':'click'}
                            ],
                            # diseño
                            'layout':{
                                'title': 'Mi gráfico con Dash'
                            }
                        }
                    ),
                ]
            )

        ]
        )
    ])

])
