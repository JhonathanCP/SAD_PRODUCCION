import pandas as pd
import pymysql.cursors
from plotly.offline import plot
import plotly.graph_objs as go

def plotly_plot(postgresql_connection):
    sql="""SELECT * FROM DB"""
    
    with postgresql_connection.cursor() as cursor:
        cursor.execute(sql)
        row=cursor.fetchall()

    result_table=pd.DataFrame(row)

    fig=go.Figure(data = go.Bar(name='Plot1', x=result_table['Column1'], y=result_table['Column2']))

    fig.update_layout(title_text='Plotly_Plot1',
    xaxis_title='X_Axis',yaxis_title='Y_Axis')

    plotly_plot_obj= plot({'data':fig}, output_type='div')

    return plotly_plot_obj

    