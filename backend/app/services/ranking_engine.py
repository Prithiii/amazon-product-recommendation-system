import pandas as pd
from sqlalchemy import create_engine


def get_ranked_products():

    engine = create_engine(
        "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
    )

    query = """
    SELECT
        product_id,
        avg_rating,
        rating_count,
        popularity_score
    FROM recommendation_logic
    ORDER BY popularity_score DESC
    LIMIT 20;
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")