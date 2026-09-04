from fastapi import APIRouter
from app.services.recommendation_engine import get_hybrid_recommendations

router = APIRouter()

@router.get("/hybrid/{user_id}")
def hybrid_recommendation(user_id: str):

    return get_hybrid_recommendations(user_id)