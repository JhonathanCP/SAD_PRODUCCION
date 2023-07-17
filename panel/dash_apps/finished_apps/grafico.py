
import dash
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go

app = DjangoDash('grafico',external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = go.Figure()

df = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [1, 4, 2, 3, 5]})

app.layout = dbc.Container(children =   
    [
        html.Br(),
        html.H1("Dashboard"),
        html.Br(),
        dbc.Row(children = [
            dbc.Col(
            html.Div(
                    id = 'div_dropdown',
                    children = [
                        dcc.Dropdown(
                            id = 'iddropdown',
                            options = [],   
                            value ='',         
                            placeholder = 'selecciona un valor',                                                                                
                        )
                    ],style={'padding-bottom': '30px'}
                ),xs=12,sm=6,md=6,lg=3,xl=2
            ),
        ]),
        dbc.Row(children=
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Título de la tarjeta 1", className="card-title"),
                                        html.P(
                                            "Texto de la tarjeta 1. Aquí puedes agregar cualquier contenido que quieras.", className="card-text"
                                        ),
                                        dbc.Button("Haz clic aquí", color="primary"),
                                    ], style = {"background-color": "silver"}
                                )
                            ]
                        )
                    ],
                    width=4,
                    className="mb-4"
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Título de la tarjeta 1", className="card-title"),
                                        html.P(
                                            "Texto de la tarjeta 1. Aquí puedes agregar cualquier contenido que quieras.", className="card-text"
                                        ),
                                        dbc.Button("Haz clic aquí", color="primary"),
                                    ], style = {"background-color": "silver"}
                                )
                            ]
                        )
                    ],
                    width=4,
                    className="mb-4"
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Título de la tarjeta 1", className="card-title"),
                                        html.P(
                                            "Tarjeta 2, prueba de tamaño, opacidad de 0.3 ", className="card-text"
                                        ),
                                        dbc.Button("Haz clic aquí", color="primary"),
                                    ], style = {"background-color": "silver"}
                                )
                            ]
                        )
                    ],
                    width=4,
                    className="mb-5"
                )
            ]
        ),
        dbc.Row(children=
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Título de la tarjeta 1", className="card-title"),
                                        html.P(
                                            "Texto de la tarjeta 1. Aquí puedes agregar cualquier contenido que quieras.", className="card-text"
                                        ),
                                        dbc.Button("Haz clic aquí", color="primary"),
                                    ], style = {"background-color": "silver"}
                                )
                            ]
                        )
                    ],
                    width=4,
                    className="mb-4"
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Título de la tarjeta 1", className="card-title"),
                                        html.P(
                                            "Texto de la tarjeta 1. Aquí puedes agregar cualquier contenido que quieras.", className="card-text"
                                        ),
                                        dbc.Button("Haz clic aquí", color="primary"),
                                    ], style = {"background-color": "silver"}
                                )
                            ]
                        )
                    ],
                    width=4,
                    className="mb-4"
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Título de la tarjeta 1", className="card-title"),
                                        html.P(
                                            "Texto de la tarjeta 1. Aquí puedes agregar cualquier contenido que quieras.", className="card-text"
                                        ),
                                        dbc.Button("Haz clic aquí", color="primary"),
                                    ], style = {"background-color": "silver"}
                                )
                            ]
                        )
                    ],
                    width=4,
                    className="mb-4"
                )
            ]
        ),
        dbc.Row(children=
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Título de la tarjeta 1", className="card-title"),
                                        html.P(
                                            "Texto de la tarjeta 1. Aquí puedes agregar cualquier contenido que quieras.", className="card-text"
                                        ),
                                        dbc.Button("Haz clic aquí", color="primary"),
                                    ], style = {"background-color": "silver"}
                                )
                            ]
                        )
                    ],
                    width=4,
                    className="mb-4"
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Título de la tarjeta 1", className="card-title"),
                                        html.P(
                                            "Texto de la tarjeta 1. Aquí puedes agregar cualquier contenido que quieras.", className="card-text"
                                        ),
                                        dbc.Button("Haz clic aquí", color="primary"),
                                    ], style = {"background-color": "silver"}
                                )
                            ]
                        )
                    ],
                    width=4,
                    className="mb-4"
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Título de la tarjeta 1", className="card-title"),
                                        html.P(
                                            "Texto de la tarjeta 1. Aquí puedes agregar cualquier contenido que quieras.", className="card-text"
                                        ),
                                        dbc.Button("Haz clic aquí", color="primary"),
                                    ], style = {"background-color": "silver"}
                                )
                            ]
                        )
                    ],
                    width=4,
                    className="mb-4"
                )
            ]
        )
        
    ]
)

    