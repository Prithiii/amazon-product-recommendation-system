from fastapi import APIRouter
from sqlalchemy import create_engine
import pandas as pd

router = APIRouter()

engine = create_engine(
    "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
)

@router.get("/analytics")
def analytics():

    total_users = pd.read_sql(
        "SELECT COUNT(DISTINCT user_id) as count FROM recommendation_logs",
        engine
    )["count"][0]

    total_recommendations = pd.read_sql(
        "SELECT COUNT(*) as count FROM recommendation_logs",
        engine
    )["count"][0]

    top_products = pd.read_sql(
        """
        SELECT
            recommended_product,
            COUNT(*) as recommendation_count
        FROM recommendation_logs
        GROUP BY recommended_product
        ORDER BY recommendation_count DESC
        LIMIT 10
        """,
        engine
    )

    return {
        "total_users": int(total_users),
        "total_recommendations": int(total_recommendations),
        "top_products": top_products.to_dict(orient="records")
    }