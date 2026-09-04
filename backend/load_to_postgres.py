import pandas as pd
from sqlalchemy import create_engine

# Replace with your PostgreSQL password
DB_PASSWORD = "Admin"

engine = create_engine(
    f"postgresql://postgres:{DB_PASSWORD}@localhost:5432/amazon_recommender"
)

print("Reading parquet file...")

df = pd.read_parquet(
    "data/processed/electronics_sample.parquet"
)

df = df.rename(
    columns={
        "parent_asin": "product_id",
        "timestamp": "review_timestamp"
    }
)

print(df.head())

print("Loading into PostgreSQL...")

df.to_sql(
    "interactions",
    engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=10000
)

print("Load completed successfully!")