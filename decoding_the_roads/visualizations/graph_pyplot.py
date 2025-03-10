from plotly import express as px
from plotly.graph_objs import Figure
from pandas import DataFrame , to_numeric , read_sql
from ..utils.logger import setup_logger
from typing import List
logger = setup_logger(__name__)

def sqlquery_to_dataframe(sql_query: str, x , y , conn=None ) -> DataFrame:
    """ 
    Function to convert the result of a SQL query to a DataFrame
    args:
        sql_query: str
        conn: Connection
    returns:
        df: DataFrame
    """
    try:
        # df: DataFrame = DataFrame(read_sql(sql_query, conn))
        df: DataFrame = DataFrame(sql_query)
        # Check if `data` is a list of tuples, then convert it to DataFrame with correct column names
        if isinstance(sql_query, list) and isinstance(sql_query[0], tuple):
            df = DataFrame(sql_query, columns=[x, y])  # Explicitly set column names
        else:
            df = DataFrame(sql_query)

        logger.info(f"df: {df}")

        # Check if x and y exist in DataFrame
        if x not in df.columns or y not in df.columns:
            raise ValueError(f"Columns '{x}' or '{y}' not found in data.")
        
        df[y] = to_numeric(df[y])
        df.sort_values(by=y, ascending=True)
        return df
    except Exception as e:
        logger.error(f"Error in sqlquery_to_dataframe: {e}")

# Line Chart
def line_chart(data, x: str, y: str, title: str) -> Figure:
    """ 
    Function to create a line chart
    args: 
        data: Dict`
        x: str
        y: str
        title
    returns:
        fig: Figure

    """
    try:

        df = sqlquery_to_dataframe(data, x, y)

        fig = px.line(df, x=x, y=y, title=title)
        return fig
    except Exception as e:
        logger.error(f"Error in line_chart: {e}")

# Bar Chart
def bar_chart(data, x: str, y: str, title: str):
    """ 
    Function to create a bar chart
    args:
        data: List of Tuples (or DataFrame)
        x: str (Column for X-axis)
        y: str (Column for Y-axis)
        title: str (Chart Title)

    returns:
        fig: Figure 
    """
    try:

        # Sort y-axis from 0 to 7
        df = sqlquery_to_dataframe(data, x, y)
        # Create Bar Chart
        fig = px.bar(df, x=x, y=y, title=title)
        return fig

    except Exception as e:
        logger.error(f"Error in bar_chart: {e}")
# Scatter Plot
def scatter_plot(data, x: str, y: str, title: str) -> Figure:
    """ 
    Function to create a scatter plot
    args:
        data: Dict
        x: str
        y: str
        title: str

    returns:
        fig: Figure 
    """
    try:
        
        df = sqlquery_to_dataframe(data, x, y)
        fig: Figure = px.scatter(df, x=x, y=y, title=title, color=y, size=y)
        return fig
    except Exception as e:
        logger.error(f"Error in scatter_plot: {e}")

# Pie Chart
def pie_chart(data, names: str, values: str, title: str) -> Figure:
    """ 
    Function to create a pie chart
    args:
        data: Dict
        x: str
        y: str
        title: str

    returns:
        fig: Figure 
    """
    try:
        df = sqlquery_to_dataframe(data, x, y)
        fig: Figure = px.pie(df, names=names, values=values, title=title, hole=0.3)
        return fig
    except Exception as e:
        logger.error(f"Error in pie_chart: {e}")

# Bubble Chart
def bubble_chart(data, x: str, y: str, size: str, title: str) -> Figure:
    """ 
    Function to create a bubble chart
    args:
        data: Dict
        x: str
        y: str
        title: str

    returns:
        fig: Figure 
    """
    try:
        df = sqlquery_to_dataframe(data, x, y)
        fig: Figure = px.scatter(df, x=x, y=y, size=size, color=size, title=title)
        return fig
    except Exception as e:
        logger.error(f"Error in bubble_chart: {e}")

# Categorical Axes Chart
def categorical_axes_chart(data, x: str, y: str, category: str, title: str) -> Figure:
    """ 
    Function to create a categorical axes chart
    args:
        data: Dict
        x: str
        y: str
        category: str
        title: str
    returns:
        fig: Figure 
    """
    try:
        df = sqlquery_to_dataframe(data, x, y)
        fig: Figure = px.bar(df, x=x, y=y, color=category, title=title, barmode="group")
        return fig
    except Exception as e:
        logger.error(f"Error in categorical_axes_chart: {e}")


if __name__ == "__main__":
    fig = line_chart(data={'x': [1, 2, 3, 4, 5], 'y': [2, 4, 1, 5, 3]}, x='x', y='y', title='Sample Plotly Chart')
    fig.write_image("./output/line_chart.png")
    #logger.error(fig)


