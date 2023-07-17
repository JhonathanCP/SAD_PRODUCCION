from django_plotly_dash import DjangoDash
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

external_stylesheets = ['https:codepen.io/chriddyp/pen/bWLwgP.css']
app=DjangoDash('pruebacallback',external_stylesheets=external_stylesheets)

app.layout=html.Div(children=[
    dcc.Input(
        id='my_input',
        placeholder='Introduzca su nombre',
        value='',
        type='text'
    ),
    dcc.Dropdown(
        id='dropdown-component',
        options=[
            {'label':'Big data', 'value':'bigdata'},
            {'label': 'Data Science', 'value': 'datascience'},
            {'label': 'Bases de Datos', 'value': 'database'},
            {'label': 'Web', 'value': 'web'}
        ],
        placeholder="Selecciona la/s categoría/s",
        multi=False,
        searchable=False,
        value='bigdata',
        disabled=False,
        className='three columns'
    ),
    html.Button(
        id='buttom',
        n_clicks=0,
        children="Enviar"
    ),
    html.Div(
        id='res_input',
        className='twelve columns'
    ),
    html.Div(
        id='res_input2',
        className='twelve columns'
    )
])


# CALLBACKS

# @app.callback(
#     # [dash.dependencies.Output('id_del_div_donde_se_colocará_el_contenido', 'la_propiedad=children')]
#     [dash.dependencies.Output('res_input','children'),
#     dash.dependencies.Output('res_input2','children')],
#     # de donde se tomará el valor a ingresar
#     [dash.dependencies.Input('my_input','value'),
#     dash.dependencies.Input('dropdown-component','value')]
# ) 
# #defino el metodo que va realizar esa modificacion
# # va a recibir 2 parametros(los dos parametros de las entradas)
# def update_value(nombre,categoria):
#     return (html.H3(f'Hola {nombre}: la categoria es {categoria}'),
#     html.H6(f"Hola {nombre.capitalize()}: La categoria es {categoria}")
#     )

# -------------------------
# ESTADOS

@app.callback(
    # [dash.dependencies.Output('id_del_div_donde_se_colocará_el_contenido', 'la_propiedad=children')]
    [dash.dependencies.Output('res_input','children'),
    dash.dependencies.Output('res_input2','children')],
    [dash.dependencies.Input('buttom','n_clicks')],
    # de donde se guardará el valor a ingresar
    [dash.dependencies.State('my_input','value'),
    dash.dependencies.State('dropdown-component','value')]
) 
#defino el metodo que va realizar esa modificacion
# va a recibir 2 parametros(los dos parametros de las entradas)
def update_value(n_clicks,nombre,categoria):
    return (html.H3(f'Hola {nombre}: la categoria es {categoria}. Numero de clicks: {n_clicks}'),
    html.H6(f"Hola {nombre.capitalize()}: La categoria es {categoria}")
    )