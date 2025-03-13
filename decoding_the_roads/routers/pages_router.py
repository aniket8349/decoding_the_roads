import json
import os
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from mysql.connector import MySQLConnection
from fastapi.templating import Jinja2Templates
import plotly.express as px
import pandas as pd

from ..utils.sql_utils import fetch_query_results, execute_query;
from ..config.db_config import db_config
from ..visualizations.graph_pyplot import line_chart , bar_chart, scatter_plot, pie_chart, bubble_chart
from ..utils.sqlquery_to_json import sqlquery_to_json
from ..utils.logger import setup_logger
from ..utils.read_json import read_json_file

from ..constant.constant import CONTENT_JSON

router = APIRouter()
templates = Jinja2Templates(directory="decoding_the_roads/templates")

logger = setup_logger(__name__) 
file_path = os.path.join(CONTENT_JSON, "content.json")

@router.get("/")
async def read_items(request: Request):
    try:
        return templates.TemplateResponse("pages/main.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    try:
        # Sample data (replace with your data loading/analysis)
        
        return templates.TemplateResponse("pages/dashboard.html", {"request": request})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard-index", response_class=HTMLResponse)
async def reports(request: Request):
    # data = {'x': [1, 2, 3, 4, 5], 'y': [2, 4, 1, 5, 3]}

    try:
        query = "SELECT Location , Casualties FROM global_traffic_accidents LIMIT 4;"
        query_result = fetch_query_results(db_config, query)
        logger.info(query_result)
        
        fig = bar_chart(data=query_result, x='location', y='casualties', title='Sample Plotly Chart')
        fig.update_layout(autosize=True)
        plotly_html  =  fig.to_html(include_plotlyjs="cdn")
        return templates.TemplateResponse("/components/dashboard-index.html", {"request": request , "plotly_html": plotly_html})

    except Exception as e:
        logger.error(f"An error occurred: {str(e)} ")
        raise HTTPException(status_code=500, detail=str(e))
   
@router.get("/chart", response_class=HTMLResponse)
def reports(request: Request):
    try:
        query = "SELECT Location , Casualties FROM global_traffic_accidents LIMIT 4;"
        query_result = fetch_query_results(db_config, query)
        logger.info(query_result)
        fig = bar_chart(data=query_result, x='location', y='casualties', title='Sample Plotly Chart')
        plotly_html  =  fig.to_html(include_plotlyjs="cdn")
        
        json_data = read_json_file(file_path)
        chart_data = {
        "chart_card1": {
            "chart_title": json_data.get("chart_card1").get("chart_title"),
            "chart_data": json_data.get("chart_card1").get("chart_data"),
            "chart_html": plotly_html,
        }
    }      
        return templates.TemplateResponse("/components/chart.html", {"request": request , "chart_data": chart_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@router.get("/analysis/diagnostic", response_class=HTMLResponse)
def reports(request: Request):
    try:
        return templates.TemplateResponse("/components/diagnostic.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/prescriptive", response_class=HTMLResponse)
def reports(request: Request):
    try:
        return templates.TemplateResponse("/components/prescriptive.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/analysis/predictive", response_class=HTMLResponse)
def reports(request: Request):
    try:
        return templates.TemplateResponse("/components/predictive.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))