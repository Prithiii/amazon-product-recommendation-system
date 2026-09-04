import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
)

query = """
SELECT
    product_id,
    AVG(rating) AS avg_rating,
    COUNT(*) AS rating_count
FROM interactions
GROUP BY product_id;
"""

stats = pd.read_sql(query, engine)
stats.to_sql(
    "product_stats",
    engine,
    if_exists="replace",
    index=False
)
print(stats.head())