from plotly import express as px
from plotly.graph_objs import Figure
from pandas import DataFrame
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

# Line Chart
def line_chart(data, x: str, y: str, title: str) -> Figure:
    try:
        df: DataFrame = DataFrame(data)
        if x not in df.columns or y not in df.columns:
            raise ValueError(f"Columns '{x}' or '{y}' not found in data.")
        fig: Figure = px.line(df, x=x, y=y, title=title)
        return fig
    except Exception as e:
        logger.error(f"Error in line_chart: {e}")

# Bar Chart
def bar_chart(data, x: str, y: str, title: str) -> Figure:
    try:
        df: DataFrame = DataFrame(data)
        if x not in df.columns or y not in df.columns:
            raise ValueError(f"Columns '{x}' or '{y}' not found in data.")
        fig: Figure = px.bar(df, x=x, y=y, title=title)
        return fig
    except Exception as e:
        logger.error(f"Error in bar_chart: {e}")

# Scatter Plot
def scatter_plot(data, x: str, y: str, title: str) -> Figure:
    try:
        df: DataFrame = DataFrame(data)
        if x not in df.columns or y not in df.columns:
            raise ValueError(f"Columns '{x}' or '{y}' not found in data.")
        fig: Figure = px.scatter(df, x=x, y=y, title=title, color=y, size=y)
        return fig
    except Exception as e:
        logger.error(f"Error in scatter_plot: {e}")

# Pie Chart
def pie_chart(data, names: str, values: str, title: str) -> Figure:
    try:
        df: DataFrame = DataFrame(data)
        if names not in df.columns or values not in df.columns:
            raise ValueError(f"Columns '{names}' or '{values}' not found in data.")
        fig: Figure = px.pie(df, names=names, values=values, title=title, hole=0.3)
        return fig
    except Exception as e:
        logger.error(f"Error in pie_chart: {e}")

# Bubble Chart
def bubble_chart(data, x: str, y: str, size: str, title: str) -> Figure:
    try:
        df: DataFrame = DataFrame(data)
        if x not in df.columns or y not in df.columns or size not in df.columns:
            raise ValueError(f"Columns '{x}', '{y}', or '{size}' not found in data.")
        fig: Figure = px.scatter(df, x=x, y=y, size=size, color=size, title=title)
        return fig
    except Exception as e:
        logger.error(f"Error in bubble_chart: {e}")

# Categorical Axes Chart
def categorical_axes_chart(data, x: str, y: str, category: str, title: str) -> Figure:
    try:
        df: DataFrame = DataFrame(data)
        if x not in df.columns or y not in df.columns or category not in df.columns:
            raise ValueError(f"Columns '{x}', '{y}', or '{category}' not found in data.")
        fig: Figure = px.bar(df, x=x, y=y, color=category, title=title, barmode="group")
        return fig
    except Exception as e:
        logger.error(f"Error in categorical_axes_chart: {e}")


if __name__ == "__main__":
    fig = line_chart(data={'x': [1, 2, 3, 4, 5], 'y': [2, 4, 1, 5, 3]}, x='x', y='y', title='Sample Plotly Chart')
    fig.write_image("./output/line_chart.png")
    #logger.error(fig)


