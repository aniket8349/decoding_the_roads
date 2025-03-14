import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from mysql.connector import MySQLConnection
from fastapi.templating import Jinja2Templates
import plotly.express as px
import pandas as pd


from ..visualizations.graph_pyplot import line_chart
from ..utils.sql_utils import fetch_query_results, execute_query;
from ..config.db_config import db_config
#from ..utils.test_plot import line_chart
from ..utils.logger import setup_logger

logger = setup_logger(__name__)  
router = APIRouter()
templates = Jinja2Templates(directory="decoding_the_roads/templates")

@router.get("/accident_trends")
async def get_accident_trends():
    try:
        # query = "CREATE TABLE test_accident_data as SELECT * FROM accident_data LIMIT 4;"
        query = "SELECT * FROM accident_data LIMIT 4;"
        query_result = fetch_query_results(db_config, query)

        # convert the query result to a json object
        # columns = ["id", "country", "accidents", "year"]
        # rows = json.loads(query_result)
        # data = [dict(zip(columns, row)) for row in rows]
        result_dict = {"x": [], "y": []}

        for row in query_result:
            result_dict["x"].append(row[1])
            result_dict["y"].append(row[2])

        try:
            logger.info(result_dict)
        except:
            logger.error("Error in logging")
        return { "query_result" : result_dict } # Convert data to JSON string

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weather_condition")
async def get_plot_by_weather_condition():
    try:
        query = "SELECT weather_condition, COUNT(*) as accident_count FROM accident_data GROUP BY weather_condition;"
        query_result = fetch_query_results(db_config, query)

        # convert the query result to a json object
        return json.dumps(query_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/app")
async def get_plot(request: Request):
    try:
        # Sample data (replace with your data loading/analysis)
        data = {'x': [1, 2, 3, 4, 5], 'y': [2, 4, 1, 5, 3]}

        # Convert dictionary to DataFrame
        df = pd.DataFrame(data)
        # Create Plotly Express chart
        fig = px.bar(df, x='x', y='y', title='Sample Plotly Chart')

        # Convert the Plotly chart to HTML
        plotly_html = fig.to_html(include_plotlyjs="cdn")  # include_plotlyjs=False is still important

        return templates.TemplateResponse("dashboard.html", {"request": request, "plotly_html": plotly_html})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
