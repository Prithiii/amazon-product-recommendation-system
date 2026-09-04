import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

from app.services.collaborative_recommender import (
    get_recommendations
)

from app.services.user_preference import (
    get_user_preference_score
)

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Admin@db:5432/amazon_recommender"
)

def save_recommendations(
    user_id,
    recommendations
):

    print(
        f"Saving {len(recommendations)} recommendations for {user_id}"
    )

    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:

        for rec in recommendations:

            print("INSERTING:", rec)

            conn.execute(
                text("""
                    INSERT INTO recommendation_logs
                    (
                        user_id,
                        recommended_product,
                        score,
                        created_at
                    )
                    VALUES
                    (
                        :user_id,
                        :product,
                        :score,
                        :created_at
                    )
                """),
                {
                    "user_id": str(user_id),

                    # SAVE PRODUCT NAME INSTEAD OF PRODUCT ID
                    "product": str(
                        rec["product_name"]
                    ),

                    "score": float(
                        rec["priority_score"]
                    ),

                    "created_at": datetime.now()
                }
            )


def get_final_rankings(user_id):

    engine = create_engine(DATABASE_URL)

    collaborative_data = get_recommendations(
        user_id
    )

    product_df = pd.read_sql(
        """
        SELECT
            rl.product_id,
            rl.popularity_score,
            pc.product_name,
            pc.category,
            pc.avg_rating
        FROM recommendation_logic rl
        LEFT JOIN product_catalog pc
            ON rl.product_id = pc.product_id
        """,
        engine
    )

    user_pref_score = (
        get_user_preference_score(user_id)
    )

    results = []

    for item in collaborative_data[
        "recommended_products"
    ]:

        product_id = item["product_id"]

        collaborative_score = float(
            item["score"]
        )

        product_row = product_df[
            product_df["product_id"]
            == product_id
        ]

        popularity_score = 0
        product_name = "Unknown Product"
        category = "Unknown"
        avg_rating = 0

        if not product_row.empty:

            popularity_score = float(
                product_row[
                    "popularity_score"
                ].iloc[0]
            )

            if pd.notna(
                product_row[
                    "product_name"
                ].iloc[0]
            ):
                product_name = str(
                    product_row[
                        "product_name"
                    ].iloc[0]
                )

            if pd.notna(
                product_row[
                    "category"
                ].iloc[0]
            ):
                category = str(
                    product_row[
                        "category"
                    ].iloc[0]
                )

            if pd.notna(
                product_row[
                    "avg_rating"
                ].iloc[0]
            ):
                avg_rating = float(
                    product_row[
                        "avg_rating"
                    ].iloc[0]
                )

        priority_score = (
            (0.5 * collaborative_score)
            + (0.3 * popularity_score)
            + (0.2 * user_pref_score)
        )

        results.append(
            {
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "avg_rating": round(
                    avg_rating,
                    2
                ),
                "collaborative_score": round(
                    collaborative_score,
                    4
                ),
                "popularity_score": round(
                    popularity_score,
                    4
                ),
                "priority_score": round(
                    priority_score,
                    4
                )
            }
        )

    results = sorted(
        results,
        key=lambda x: x[
            "priority_score"
        ],
        reverse=True
    )

    # SAVE RESULTS TO DATABASE
    save_recommendations(
        user_id,
        results
    )

    return results