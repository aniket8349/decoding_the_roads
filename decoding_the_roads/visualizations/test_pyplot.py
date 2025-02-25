from plotly import express as px
from plotly.graph_objs import Figure
from pandas import DataFrame

# line chart utility function
def line_chart(data , x: str , y: str, title: str, )-> Figure:
    df: DataFrame = DataFrame(data)
    fig: Figure = px.line(df, x=x, y=y, title=title)
    return fig

def bar_chart(data , x: str , y: str, title: str, )-> Figure:
    df: DataFrame = DataFrame(data)
    fig: Figure = px.bar(df, x=x, y=y, title=title)
    return fig



if __name__ == "__main__":
    fig = line_chart(data={'x': [1, 2, 3, 4, 5], 'y': [2, 4, 1, 5, 3]}, x='x', y='y', title='Sample Plotly Chart')
    fig.write_image("./output/line_chart.png")
    #print(fig)


