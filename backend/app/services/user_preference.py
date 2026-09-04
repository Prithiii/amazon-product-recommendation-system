import pandas as pd
from sqlalchemy import create_engine


def get_user_preference_score(user_id):

    engine = create_engine(
        "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
    )

    query = f"""
    SELECT AVG(rating) as avg_rating
    FROM interactions
    WHERE user_id = '{user_id}'
    """

    df = pd.read_sql(query, engine)

    if df.empty or df["avg_rating"].iloc[0] is None:
        return 3.0

    return float(df["avg_rating"].iloc[0])