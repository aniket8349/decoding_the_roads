from dotenv import load_dotenv
# from kaggle.api.kaggle_api_extended import KaggleApi
from fastapi import FastAPI, HTTPException 
from fastapi.staticfiles import StaticFiles
from .routers import sql_router , pages_router
from .services.startup_event import startup_event 
from .services.shutdown_event import shutdown_event
# from .config.kaggle_auth import authenticate_kaggle

load_dotenv() # loading env

app = FastAPI()
app.include_router(sql_router.router)
app.include_router(pages_router.router)
app.mount("/static", StaticFiles(directory="decoding_the_roads/static"), name="static")

# uncomment the following line to authenticate kaggle
# kaggle_api = KaggleApi()
# kaggle_api.authenticate()

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


def main():
    import uvicorn
    uvicorn.run(app="app.main:app", host="127.0.0.1", port=8000, reload=True)  # Important: app="app.main:app"


if __name__ == "__main__":
    main()