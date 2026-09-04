from fastapi import APIRouter

from app.services.evaluate_model import (
    evaluate_user
)

router = APIRouter()

@router.get("/evaluation/{user_id}")
def get_evaluation(user_id: str):

    return evaluate_user(user_id)