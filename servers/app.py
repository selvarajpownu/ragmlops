from fastapi import FastAPI
from logger.logger import logger
from routes.route import healthcheck_handler, postuserinput_handler


app = FastAPI()
origins = ["http://localhost:8000"]
logger.info("Starting API...")

app.include_router(healthcheck_handler)
app.include_router(postuserinput_handler)



