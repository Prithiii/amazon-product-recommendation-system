from fastapi import FastAPI

from app.api.recommendations import router as recommendation_router
from app.api.final_ranking import router as ranking_router
from app.api.history import router as history_router
from app.api.evaluation import (
    router as evaluation_router
)

app = FastAPI()

app.include_router(
    evaluation_router
)

app.include_router(recommendation_router)
app.include_router(ranking_router)
app.include_router(history_router)
