from django_plotly_dash import DjangoDash
from dash import html
from dash import dcc
import plotly.graph_objs as go
import pandas as pd

import dash

df= pd.read_excel("./panel/data/salesfunnel.xlsx")

mgr_options= df["Manager"].unique()

app = DjangoDash('reporte')

app.layout=html.Div([
    html.H2("Informe de embudo de ventas"),
    html.Div(
        [
            dcc.Dropdown(
                id="Manager",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options],
                value='All Managers'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
])

@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Manager', 'value')])
def update_graph(Manager):
    if Manager == "All Managers":
        df_plot = df.copy()
    else:
        df_plot = df[df['Manager'] == Manager]

    pv = pd.pivot_table(
        df_plot,
        index=['Name'],
        columns=["Status"],
        values=['Quantity'],
        aggfunc=sum,
        fill_value=0)
        
    trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'rechazado')], name='Rechazado')
    trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pendiente')], name='pendiente')
    trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presentado')], name='Presentado')
    trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'ganó')], name='Ganó')


    return {
        'data':[trace1,trace2,trace3,trace4],
        'layout':
        go.Layout(
            title='Estado del pedido del cliente para {}'.format(Manager),
            barmode='stack')
    }


