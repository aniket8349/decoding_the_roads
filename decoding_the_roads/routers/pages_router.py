import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from mysql.connector import MySQLConnection
from fastapi.templating import Jinja2Templates
import plotly.express as px
import pandas as pd


from ..utils.sql_utils import fetch_query_results, execute_query;
from ..config.db_config import db_config
from ..utils.test_plot import line_chart

router = APIRouter()
templates = Jinja2Templates(directory="decoding_the_roads/templates")


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
def reports(request: Request):
    data = {'x': [1, 2, 3, 4, 5], 'y': [2, 4, 1, 5, 3]}

    fig = line_chart(data=data, x='x', y='y', title='Sample Plotly Chart')
    plotly_html  =  fig.to_html(include_plotlyjs="cdn")
    return templates.TemplateResponse("/components/dashboard-index.html", {"request": request , "plotly_html": plotly_html})

@router.get("/chart", response_class=HTMLResponse)
def reports(request: Request):
    return templates.TemplateResponse("/components/chart.html", {"request": request})


@router.get("/analysis/diagnostic", response_class=HTMLResponse)
def reports(request: Request):
    return templates.TemplateResponse("/components/diagnostic.html", {"request": request})


@router.get("/analysis/prescriptive", response_class=HTMLResponse)
def reports(request: Request):
    return templates.TemplateResponse("/components/prescriptive.html", {"request": request})


@router.get("/analysis/predictive", response_class=HTMLResponse)
def reports(request: Request):
    return templates.TemplateResponse("/components/predictive.html", {"request": request})