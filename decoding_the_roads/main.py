from dotenv import load_dotenv
from typing import List, Optional
from kaggle.api.kaggle_api_extended import KaggleApi
from fastapi import FastAPI, HTTPException 
from fastapi.staticfiles import StaticFiles
from .routers import sql_router

from .services.startup_event import startup_event 
from .services.shutdown_event import shutdown_event


load_dotenv() # loading env


app = FastAPI()
app.include_router(sql_router.router)
app.mount("/static", StaticFiles(directory="decoding_the_roads/static"), name="static")

kaggle_api = KaggleApi()
kaggle_api.authenticate()

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

@app.get("/")
async def read_items():
    return "Hello world"

def main():
    import uvicorn
    uvicorn.run(app="app.main:app", host="0.0.0.0", port=8000, reload=True)  # Important: app="app.main:app"


if __name__ == "__main__":
    main()