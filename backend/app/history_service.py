from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Admin@db:5432/amazon_recommender"

)

def get_user_history(user_id):

    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    recommended_product,
                    score,
                    created_at
                FROM recommendation_logs
                WHERE user_id = :user_id
                ORDER BY created_at DESC
                LIMIT 20
            """),
            {"user_id": user_id}
        )

        rows = result.fetchall()

        return [
            {
                "product_id": row[0],
                "score": float(row[1]),
                "created_at": str(row[2])
            }
            for row in rows
        ]