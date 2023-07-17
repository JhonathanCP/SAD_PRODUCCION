from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash

app = DjangoDash('BarraPrueba')

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Manzanas", "Naranjas", "Platanos", "Manzanas", "Naranjas", "Platanos"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "Country": ["Perú", "Perú", "Perú", "México", "México", "México"]
})

colors = {
    'background': '#1a2d46',
    'text': '#ffffff',    
}


fig = px.bar(df, x="Fruit", y="Amount", color="Country",barmode="group", color_discrete_map={'Perú':'#119dff','México':'#66c2a5'})

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']},
children=[
    dcc.Graph(
        id='example-graph',
        animate=True,
        figure=fig, 
        style={"backgroundColor":"#1a2d46",'color':'#ffffff'}
    )
])