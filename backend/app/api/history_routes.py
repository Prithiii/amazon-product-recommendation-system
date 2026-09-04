from fastapi import APIRouter
from sqlalchemy import create_engine
import pandas as pd

router = APIRouter()

@router.get("/history/{user_id}")
def get_history(user_id: str):

    engine = create_engine(
        "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
    )

    query = f"""
        SELECT *
        FROM recommendation_logs
        WHERE user_id = '{user_id}'
        ORDER BY created_at DESC
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(
        orient="records"
    )