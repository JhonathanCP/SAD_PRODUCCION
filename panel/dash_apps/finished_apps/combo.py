import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

app = DjangoDash('combo')

app.layout = html.Div(id = 'parent', children = [
    
    #heading 
    html.H3(id = 'h3', children = 'Basic Callback example'),
    
    html.Br(),
    
    # setting dropdown
    dcc.Dropdown(id = 'dropdown',
                 options = [
                     {'label':'Exelent', 'value':5},
                     {'label':'Average','value':3},
                     {'label':'Below Average', 'value':1}
                     
                     ],
                  value = 5,
                                  
                 ),
    html.Br(),
    
    # setting div component for returning the output 
    html.Div(id = 'output-text')
    
    
    ])

@app.callback(Output(component_id='output-text',component_property='children'),
              [Input(component_id='dropdown',component_property='value')])
#define the callback function 
def basic_callback(input_value):
    return input_value