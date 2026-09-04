import pandas as pd
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Admin@db:5432/amazon_recommender"
)

engine = create_engine(DATABASE_URL)


def precision_at_k(recommended, actual, k=10):

    recommended_k = recommended[:k]

    relevant = len(
        set(recommended_k).intersection(set(actual))
    )

    return relevant / k


def recall_at_k(recommended, actual, k=10):

    recommended_k = recommended[:k]

    relevant = len(
        set(recommended_k).intersection(set(actual))
    )

    if len(actual) == 0:
        return 0

    return relevant / len(actual)


def hit_rate(recommended, actual, k=10):

    recommended_k = recommended[:k]

    return int(
        len(
            set(recommended_k).intersection(set(actual))
        ) > 0
    )


def evaluate_user(user_id):

    from app.services.collaborative_recommender import (
        get_recommendations
    )

    recommendations = get_recommendations(user_id)

    recommended_products = [
        item["product_id"]
        for item in recommendations["recommended_products"]
    ]

    actual_df = pd.read_sql(
        f"""
        SELECT product_id
        FROM interactions
        WHERE user_id = '{user_id}'
        """,
        engine
    )

    actual_products = (
        actual_df["product_id"].tolist()
        if not actual_df.empty
        else []
    )

    precision = precision_at_k(
        recommended_products,
        actual_products,
        10
    )

    recall = recall_at_k(
        recommended_products,
        actual_products,
        10
    )

    hit = hit_rate(
        recommended_products,
        actual_products,
        10
    )

    return {
        "user_id": user_id,
        "precision_at_10": round(
            precision,
            4
        ),
        "recall_at_10": round(
            recall,
            4
        ),
        "hit_rate": hit
    }


if __name__ == "__main__":

    sample_user = (
        "AE224GVO7OHTYF26U6ER6BEVIUAQ"
    )

    results = evaluate_user(sample_user)

    print(results)