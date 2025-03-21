import pandas as pd
from plotly import express as px
from plotly.graph_objs import Figure
from pandas import DataFrame , to_numeric , read_sql
from ..utils.logger import setup_logger
from typing import List, Union
logger = setup_logger(__name__)

def sqlquery_to_dataframe(sql_query, x: str, y: Union[List[str], str], conn=None) -> pd.DataFrame:
    """ 
    Convert SQL query result or list of tuples into a DataFrame.

    Args:
        sql_query (str | list | DataFrame): SQL query string or already fetched data.
        x (str): Column name for X-axis (category).
        y (list | str): Single column or list of columns for Y-axis.
        conn (optional): Database connection object.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    try:
        # Execute SQL query if a database connection is provided
        # if conn:
        #     df = pd.read_sql(sql_query, conn)
        # else:
        #     df = pd.DataFrame(sql_query)  # Assuming sql_query is pre-fetched data

        # # Handle empty or invalid data
        # if df.empty:
        #     logger.warning("SQL query returned no data.")
        #     return pd.DataFrame(columns=[x] + ([y] if isinstance(y, str) else y))

        # # If data is a list of tuples, set correct column names dynamically
        # if isinstance(sql_query, list) and all(isinstance(row, tuple) for row in sql_query):
        #     column_count = len(sql_query[0])

        #     # If `y` is a string, convert it to a list
        #     if isinstance(y, str):
        #         y = [y]

        #     expected_columns = [x] + y

        #     if column_count != len(expected_columns):
        #         raise ValueError(f"Expected {len(expected_columns)} columns ({expected_columns}), but got {column_count}.")

        #     df = pd.DataFrame(sql_query, columns=expected_columns)

        # # Validate that required columns exist
        # missing_cols = {x} | set(y) - set(df.columns)
        # if missing_cols:
        #     raise ValueError(f"Missing columns in data: {missing_cols}")

        # # Convert `x` column to string (for categorical values)
        # df[x] = df[x].astype(str)

        # # Convert `y` columns to numeric where applicable
        # for col in y:
        #     df[col] = pd.to_numeric(df[col], errors='coerce')

        # # Sort by first Y-column if multiple columns are present
        # df.sort_values(by=y[0], ascending=True, inplace=True)

        # logger.info(f"DataFrame created successfully:\n{df.head()}")
        # return df
        df = pd.DataFrame(sql_query)

        # If DataFrame has only numerical column names, assign correct column names
        if list(df.columns) == list(range(len(df.columns))):  # Checks if columns are [0, 1] or similar
            df.columns = [x] + ([y] if isinstance(y, str) else y)  

        print(df.columns.tolist())  # Debugging output
        # return df
        # [x] + ([y] if isinstance(y, str) else y)
        return pd.DataFrame(sql_query, columns=df.columns.tolist())

    except Exception as e:
        logger.error(f"Error in sqlquery_to_dataframe: {e}")
        return pd.DataFrame(columns=[x] + ([y] if isinstance(y, str) else y))  # Return empty DataFrame on failure

# chart theme
def apply_chart_theme(fig, theme: str = "light") -> Figure:
    """Apply a global theme to a Plotly figure based on the user's system preference."""
    themes = {
        "dark": {
            "bg_color": "#1F2937",
            "inner_plot_color": "#374151",
            "grid_color": "#4B5563",
            "text_color": "white"
        },
        "light": {
            "bg_color": "#FFFFFF",
            "inner_plot_color": "#F3F4F6",
            "grid_color": "#D1D5DB",
            "text_color": "black"
        }
    }

    selected_theme = themes.get(theme, themes["light"])  # Default to light mode
    grid_width = 0.5

    fig.update_layout(
        paper_bgcolor=selected_theme["bg_color"],  
        plot_bgcolor=selected_theme["inner_plot_color"],  
        font=dict(color=selected_theme["text_color"]),  
        title=dict(font=dict(size=20)),
        xaxis=dict(
            showgrid=True, gridcolor=selected_theme["grid_color"], gridwidth=grid_width,
            zeroline=True, zerolinecolor=selected_theme["grid_color"], zerolinewidth=1
        ),
        yaxis=dict(
            showgrid=True, gridcolor=selected_theme["grid_color"], gridwidth=grid_width,
            zeroline=True, zerolinecolor=selected_theme["grid_color"], zerolinewidth=1
        ),
    )
    return fig


# Line Chart
def line_chart(data, x: str, y: list, title: str, theme: str ) -> Figure:
    """ 
    Function to create a line chart with multiple lines
    args: 
        data: SQL query result (list of tuples or DataFrame)
        x: str (Column for X-axis)
        y: list (Columns for Y-axis, multiple lines)
        title: str (Chart Title)

    returns:
        fig: Plotly Figure
    """
    try:
        df = sqlquery_to_dataframe(data, x, y)

        # Convert DataFrame to long format for multiple lines
        df_melted = df.melt(id_vars=[x], value_vars=y, var_name="Metric", value_name="Value")

        # Create line chart with multiple lines
        fig = px.line(df_melted, 
                      x=x, 
                      y="Value", 
                      color="Metric",  # Differentiate by 'Metric' column
                      markers=True,
                      title=title,
                      labels={x: "Date", "Value": "Count"})  # Correct axis labels
        apply_chart_theme(fig, theme)  # Apply global theme
        return fig

    except Exception as e:
        logger.error(f"Error in line_chart: {e}")
        return None  # Return None in case of an error

# Bar Chart
def bar_chart(data, x: str, y: str, title: str, theme: str ):
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
        fig = px.bar(df, x, y, title=title)
        apply_chart_theme(fig, theme)  # Apply global theme

        return fig

    except Exception as e:
        logger.error(f"Error in bar_chart: {e}")

# Scatter Plot
def scatter_plot(data, x: str, y: str, title: str, theme: str ) -> Figure:
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
        apply_chart_theme(fig, theme)  # Apply global theme
        return fig
    except Exception as e:
        logger.error(f"Error in scatter_plot: {e}")

# Pie Chart
def pie_chart(data, names: str, values: str, title: str , theme: str ) -> Figure:
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
        df = sqlquery_to_dataframe(data, names, values)
        fig: Figure = px.pie(df, names=names, values=values, title=title, hole=0.3)
        apply_chart_theme(fig, theme)  # Apply global theme
        return fig
    
    except Exception as e:
        logger.error(f"Error in pie_chart: {e}")

# Bubble Chart
def bubble_chart(data, x: str, y: str, size: str, title: str, theme: str ) -> Figure:
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
        apply_chart_theme(fig, theme)  # Apply global theme
        return fig
    except Exception as e:
        logger.error(f"Error in bubble_chart: {e}")

# Categorical Axes Chart
def categorical_axes_chart(data, x: str, y: str, category: str, title: str, theme: str ) -> Figure:
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
        apply_chart_theme(fig, theme)  # Apply global theme
        return fig
    except Exception as e:
        logger.error(f"Error in categorical_axes_chart: {e}")

# density_heatmap

def density_heatmap(data, x: str, y: str, z: str, title: str, theme: str ) -> Figure:
    """ 
    Function to create a density heatmap
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
        fig: Figure = px.density_heatmap(df, x=x, y=y, z=z, title=title ,  color_continuous_scale="Blues")
        apply_chart_theme(fig, theme)  # Apply global theme
        return fig
    except Exception as e:
        logger.error(f"Error in density_heatmap: {e}")

if __name__ == "__main__":
    fig = line_chart(data={'x': [1, 2, 3, 4, 5], 'y': [2, 4, 1, 5, 3]}, x='x', y='y', title='Sample Plotly Chart')
    fig.write_image("./output/line_chart.png")
    #logger.error(fig)


