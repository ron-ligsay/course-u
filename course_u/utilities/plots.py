import plotly.express as px
from plotly.offline import plot

def generate_pie_chart(data, title):
    fig = px.pie(
        values=list(data.values_list("total_correct", flat=True)),
        names=list(data.values_list("field_name", flat=True)),
        #title=title,
        height=500,
        width=600,
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    
    return fig

