from fastapi import APIRouter
from app.services.recommendation_engine import get_hybrid_recommendations

router = APIRouter()

@router.get("/ranked/{user_id}")
def ranked(user_id: str):
    try:
        return get_hybrid_recommendations(user_id)
    except Exception as e:
        return {"error": str(e)}