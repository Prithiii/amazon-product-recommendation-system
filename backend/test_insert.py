# test_insert.py

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
)

df = pd.DataFrame([
    {
        "user_id": "TEST_USER",
        "recommended_product": "TEST_PRODUCT",
        "score": 99.9
    }
])

df.to_sql(
    "recommendation_logs",
    engine,
    if_exists="append",
    index=False
)

print("Inserted successfully")