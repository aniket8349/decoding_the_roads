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
from ..data_analysis.common_causes import common_accident_causes
from ..data_analysis.accidents_year import accidents_and_casualties_by_month , yearly_accident_trends , derived_accident_severity
from ..data_analysis.diagnostic_analysis.eda import check_missing_values ,  check_missing_value_for_accident_id , remove_missing_values , remove_duplicates 
from ..data_analysis.diagnostic_analysis.diagnostic_report import get_avg_casualties_by_weather, get_accident_counts_by_time_period, get_top_accident_prone_locations , get_accidents_clear_vs_rainy , get_avg_vehicles_by_road_condition , get_common_accident_causes , get_locations_needing_safety_improvements
from ..data_analysis.diagnostic_analysis.prespective_report import get_accident_hotspots , get_high_risk_times , get_weather_related_accidents , get_high_severity_accidents
from ..constant.constant import CONTENT_JSON , DIAGNOSTIC_ANALYSIS , PERSPECTIVE_ANALYSIS
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
        card_data = {
            "card1": {
                "title": "Total Accidents",
                "value": 1000,
                "icon": "fas fa-car-crash",
                "color": "primary",
            },
            "card2": {
                "title": "Total Casualties",
                "value": 500,
                "icon": "fas fa-ambulance",
                "color": "danger",
            },
            "card3": {
                "title": "Total Vehicles",
                "value": 2000,
                "icon": "fas fa-car",
                "color": "warning",
            },
            "card4": {
                "title": "Total Persons",
                "value": 1500,
                "icon": "fas fa-user",
                "color": "success",
            },
        }
        casualties_by_month = common_accident_causes(db_config)
        
        fig = line_chart(data=casualties_by_month, x='Cause', y=['Total_Accidents' , 'Total_Casualties'], title='Common Accident Causes').to_html(include_plotlyjs="cdn")
        # fig.update_layout(autosize=True)
        plotly_html  = fig
        return templates.TemplateResponse(
            "/components/dashboard-index.html", 
            {
                "request": request , 
                "plotly_html": plotly_html,
                "card_data": card_data
            })

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
        # eda ()
        eda_mising_values = check_missing_values(db_config)
        # Root Cause & Comparative Analysis
        accident_counts_by_time_period = get_accident_counts_by_time_period(db_config)
        avg_casualties_by_weather = get_avg_casualties_by_weather(db_config)
        accident_prone_locations = get_top_accident_prone_locations(db_config)
        # Hypothesis Testing
        accidents_clear_vs_rainy = get_accidents_clear_vs_rainy(db_config)
        avg_vehicles_by_road_condition = get_avg_vehicles_by_road_condition(db_config)
        # Insights & Recommendations
        common_accident_causes = get_common_accident_causes(db_config)
        locations_needing_safety_improvements = get_locations_needing_safety_improvements(db_config)
        # Create Plotly charts
        charts = {
            "get_top_accident_prone_locations": line_chart(accident_prone_locations, "Location", ["Accident Count", "Total Casualties"], "Top Accident Prone Locations").to_html(include_plotlyjs="cdn"),
            "get_most_dangerous_times": bar_chart(accident_counts_by_time_period, "TimePeriod", "Accident Count", "Accident Count by Time Period").to_html(include_plotlyjs="cdn"),
            "get_most_dangerous_weather_conditions": bar_chart(avg_casualties_by_weather, "Weather Condition", "Avg_Casualties", "Avg Casualties by Weather").to_html(include_plotlyjs="cdn"),
            # Hypothesis Testing
            "get_accidents_clear_vs_rainy": bar_chart(accidents_clear_vs_rainy, "Weather Condition", "Accident Count", "Accident Count by Weather Condition").to_html(include_plotlyjs="cdn"),
            "get_avg_vehicles_by_road_condition": bar_chart(avg_vehicles_by_road_condition, "Road Condition", "Avg_Vehicles", "Avg Vehicles by Road Condition").to_html(include_plotlyjs="cdn"),
            # Insights & Recommendations
            "get_common_accident_causes": bar_chart(common_accident_causes, "Cause", "Accident Count", "Accident Count by Cause").to_html(include_plotlyjs="cdn"),
            "get_locations_needing_safety_improvements": bar_chart(locations_needing_safety_improvements, "Location", "Accident Count", "Accident Count by Location").to_html(include_plotlyjs="cdn"),
            
        }

   
        # Read diagnostic analysis JSON
        diagnostic_analysis_content = read_json_file(DIAGNOSTIC_ANALYSIS)

        return templates.TemplateResponse(
            "/components/diagnostic.html",
            {
                "request": request,
                "missing_data": eda_mising_values,
                "diagnostic_analysis": diagnostic_analysis_content["diagnostic_analysis"],
                "charts": charts
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/prescriptive", response_class=HTMLResponse)
def reports(request: Request):
    try:
        accident_hotspots = get_accident_hotspots(db_config)
        high_risk_times = get_high_risk_times(db_config)
        weather_related_accidents = get_weather_related_accidents(db_config)
        high_severity_accidents = get_high_severity_accidents(db_config)

        prescriptive_chart =  {
            "accident_hotspots": bar_chart(accident_hotspots, "Location", "Accident Count", "Accident Hotspots").to_html(include_plotlyjs="cdn"),
            "high_risk_times": bar_chart(high_risk_times, "Hour", "Accident Count", "High Risk Times").to_html(include_plotlyjs="cdn"),
            "weather_related_accidents": bar_chart(weather_related_accidents, "Weather Condition", "Accident Count", "Weather Related Accidents").to_html(include_plotlyjs="cdn"),
            "high_severity_accidents": bar_chart(high_severity_accidents, "Road Condition", "Avg Casualties", "High Severity Accidents").to_html(include_plotlyjs="cdn"),
        }

        prescriptive_analysis_content = read_json_file(PERSPECTIVE_ANALYSIS)
        

        return templates.TemplateResponse(
            "/components/prescriptive.html", 
            {
                "request": request,
                "prescriptive_analysis": prescriptive_analysis_content["prescriptive_analysis"],
                "charts": prescriptive_chart
            }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/analysis/predictive", response_class=HTMLResponse)
def reports(request: Request):
    try:
        return templates.TemplateResponse("/components/predictive.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))