import json
import os
from fastapi import APIRouter, HTTPException, Request , Response
from fastapi.responses import HTMLResponse , JSONResponse
from mysql.connector import MySQLConnection
from fastapi.templating import Jinja2Templates
import plotly.express as px
import pandas as pd

from ..utils.sql_utils import fetch_query_results, execute_query;
from ..config.db_config import db_config
from ..visualizations.graph_pyplot import line_chart , bar_chart, scatter_plot, pie_chart, bubble_chart, density_heatmap
from ..utils.sqlquery_to_json import sqlquery_to_json
from ..utils.logger import setup_logger
from ..utils.read_json import read_json_file
from ..utils.convert_markdown import convert_markdown_fields
from ..data_analysis.common_causes import common_accident_causes
from ..data_analysis.accidents_year import accidents_and_casualties_by_month , yearly_accident_trends , derived_accident_severity
from ..data_analysis.diagnostic_analysis.eda import check_missing_values ,  check_missing_value_for_accident_id , remove_missing_values , remove_duplicates 
from ..data_analysis.diagnostic_analysis.diagnostic_report import get_avg_casualties_by_weather, get_accident_counts_by_time_period, get_top_accident_prone_locations , get_accidents_clear_vs_rainy , get_avg_vehicles_by_road_condition , get_common_accident_causes , get_locations_needing_safety_improvements
from ..data_analysis.diagnostic_analysis.prespective_report import get_accident_hotspots , get_high_risk_times , get_weather_related_accidents , get_high_severity_accidents
from ..data_analysis.accidents_hotspot import accident_hotspots_by_weather , accident_hotspots_by_month
from ..data_analysis.location import location_cause_casualties , casualties_by_location_weather , casualties_by_location_road_condition
from ..data_analysis.dashboard_card_query import get_total_accidents_count , get_highest_accident_locations , get_highest_casualties_weather , get_highest_casualties_cause
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
    
@router.post("/dark-mode")
async def dark_mode(request: Request):
    try:
        cookies = request.headers.get("cookie", "")
        # Extract theme from cookies
        for cookie in cookies.split(";"):
            if "theme=" in cookie:
                theme = cookie.split("=")[1].strip()
        # print(mode)
        print(cookies)
        return JSONResponse(content={"message": f"Received mode: {cookies}"})
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
    # cookies
    theme_cookies = request.cookies.get("theme", "light")
 
    get_total_accidents = get_total_accidents_count(db_config)
    get_highest_accident_by_locations = list(get_highest_accident_locations(db_config)[0]) 
    get_highest_casualties_by_weather = list(get_highest_casualties_weather(db_config)[0])
    get_highest_casualties_by_cause = list(get_highest_casualties_cause(db_config)[0])

    # Total_Accidents 

    # tailwind color 
    get_green = "text-green-500 dark:text-green-500"
    get_red = "text-red-500 dark:text-red-500"
    try:
        card_data = {
            "card1": {
                "title": "Total Accidents",
                "value": get_total_accidents,
                "description": "Total number of accidents in year 2023 and 2024",
                "percentage_change": 12,
                "icon": "fas fa-car",
                "color": get_red,
            },
            "card2": {
                "title": "Location",
                "value": get_highest_accident_by_locations[1],
                "description": "Location with the highest accident count",
                "percentage_change": 10,
                "icon": "fas fa-ambulance",
                "color": get_red,
            },
            "card3": {
                "title": "Weather",
                "value": get_highest_casualties_by_weather[1],
                "description": "Weather condition with the highest casualties",
                "percentage_change": 5,
                "icon": "fas fa-car",
                "color": get_red,
            },
            "card4": {
                "title": "Cause",
                "value": get_highest_casualties_by_cause[1],
                "description": "Cause with the highest casualties",
                "percentage_change": 2,
                "icon": "fas fa-user",
                "color": get_red,
            },
        }
        casualties_by_month = common_accident_causes(db_config)
        
        fig = line_chart(data=casualties_by_month, x='Cause', y=['Total_Accidents' , 'Total_Casualties'], title='Common Accident Causes', theme=theme_cookies).to_html(include_plotlyjs="cdn")
        # fig.update_layout(autosize=True)

        data = {
            "Location": ["New York", "Los Angeles", "Chicago", "Houston", "Miami", "New York", "Los Angeles", "Chicago", "Houston", "Miami"],
            "Time of Day": ["Morning", "Morning", "Morning", "Morning", "Morning", "Evening", "Evening", "Evening", "Evening", "Evening"],
            "Accident Count": [120, 95, 80, 65, 70, 140, 110, 90, 85, 75]
            }
        heat_fig = density_heatmap(data=data, x='Location', y='Time of Day', z="Accident Count" ,title='Accident Frequency by Location & Time', theme=theme_cookies).to_html(include_plotlyjs="cdn")
        plotly_html  = fig
        return templates.TemplateResponse(
            "/components/dashboard-index.html", 
            {
                "request": request , 
                "plotly_html": plotly_html,
                "card_data": card_data,
                "heat_fig": heat_fig
            })

    except Exception as e:
        logger.error(f"An error occurred dashboard-index: {str(e)} ")
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
        logger.error(f"An error occurred chart: {str(e)} ")
        raise HTTPException(status_code=500, detail=str(e)) 

@router.get("/analysis/diagnostic", response_class=HTMLResponse)
def reports(request: Request):
    try:
        theme_cookies = request.cookies.get("theme", "light")
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
        # locations_needing_safety_improvements = get_locations_needing_safety_improvements(db_config)
        # Create Plotly charts
        charts = {
            "get_top_accident_prone_locations": line_chart(accident_prone_locations, "Location", ["Accident Count", "Total Casualties"], "Top Accident Prone Locations",theme=theme_cookies).to_html(include_plotlyjs="cdn"),
            "get_most_dangerous_times": line_chart(accident_counts_by_time_period, "TimePeriod", ["Accident Count"], "Accident Count by Time Period", theme=theme_cookies).to_html(include_plotlyjs="cdn"),
            "get_most_dangerous_weather_conditions": bar_chart(avg_casualties_by_weather, "Weather Condition", "Avg_Casualties", "Avg Casualties by Weather", theme=theme_cookies).to_html(include_plotlyjs="cdn"),
            # Hypothesis Testing
            "get_accidents_clear_vs_rainy": bar_chart(accidents_clear_vs_rainy, "Weather Condition", "Accident Count", "Accident Count by Weather Condition", theme=theme_cookies).to_html(include_plotlyjs="cdn"),
            "get_avg_vehicles_by_road_condition": bar_chart(avg_vehicles_by_road_condition, "Road Condition", "Avg_Vehicles", "Avg Vehicles by Road Condition", theme=theme_cookies).to_html(include_plotlyjs="cdn"),
            # Insights & Recommendations
            "get_common_accident_causes": pie_chart(common_accident_causes, "Cause", "Accident Count", "Accident Count by Cause", theme=theme_cookies).to_html(include_plotlyjs="cdn"),
            # "get_locations_needing_safety_improvements": density_heatmap(locations_needing_safety_improvements, x="Location", y="Road Condition ",z="Accident Count", title="Accident Count by Location", theme=theme_cookies).to_html(include_plotlyjs="cdn"),
            
        }

   
        # Read diagnostic analysis JSON
        diagnostic_analysis_content = read_json_file(DIAGNOSTIC_ANALYSIS)
        diagnostic_analysis_content["diagnostic_analysis"] = convert_markdown_fields(diagnostic_analysis_content["diagnostic_analysis"])
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
        logger.error(f"An error occurred /analysis/diagnostic: {str(e)} ")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/prescriptive", response_class=HTMLResponse)
def reports(request: Request):
    try:
        theme_cookies = request.cookies.get("theme", "light")

        accident_hotspots = get_accident_hotspots(db_config)
        high_risk_times = get_high_risk_times(db_config)
        weather_related_accidents = get_weather_related_accidents(db_config)
        high_severity_accidents = get_high_severity_accidents(db_config)

        prescriptive_chart =  {
            "accident_hotspots": bar_chart(accident_hotspots, "Location", "Accident Count", "Accident Hotspots", theme=theme_cookies ).to_html(include_plotlyjs="cdn"),
            "high_risk_times": bar_chart(high_risk_times, "Hour", "Accident Count", "High Risk Times", theme=theme_cookies ).to_html(include_plotlyjs="cdn"),
            "weather_related_accidents": bar_chart(weather_related_accidents, "Weather Condition", "Accident Count", "Weather Related Accidents", theme=theme_cookies ).to_html(include_plotlyjs="cdn"),
            "high_severity_accidents": bar_chart(high_severity_accidents, "Road Condition", "Avg Casualties", "High Severity Accidents", theme=theme_cookies ).to_html(include_plotlyjs="cdn"),
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
        logger.error(f"An error occurred /analysis/prescriptive: {str(e)} ")
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/analysis/predictive", response_class=HTMLResponse)
def reports(request: Request):
    try:
        return templates.TemplateResponse("/components/predictive.html", {"request": request})
    except Exception as e:
        logger.error(f"An error occurred /analysis/predictive: {str(e)} ")
        raise HTTPException(status_code=500, detail=str(e))