import pandas as pd
from sqlalchemy import create_engine


def get_popular_products():

    engine = create_engine(
        "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
    )

    query = """
    SELECT
        product_id,
        COUNT(*) AS total_reviews,
        AVG(rating) AS avg_rating
    FROM interactions
    GROUP BY product_id
    HAVING COUNT(*) >= 10
    ORDER BY avg_rating DESC, total_reviews DESC
    LIMIT 10;
    """

    df = pd.read_sql(query, engine)

    return df.to_dict(orient="records")


if __name__ == "__main__":

    results = get_popular_products()

    print(results)