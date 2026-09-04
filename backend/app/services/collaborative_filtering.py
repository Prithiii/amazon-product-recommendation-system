import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

engine = create_engine(
    "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
)

query = """
SELECT user_id, product_id, rating
FROM interactions
LIMIT 500000;
"""

df = pd.read_sql(query, engine)

print("Original Shape:", df.shape)

# Keep only active users
user_counts = df["user_id"].value_counts()
active_users = user_counts[user_counts >= 5].index
df = df[df["user_id"].isin(active_users)]

print("Filtered Shape:", df.shape)
print("Unique Users:", df["user_id"].nunique())
print("Unique Products:", df["product_id"].nunique())

print("Building user-item matrix...")

user_item_matrix = df.pivot_table(
    index="user_id",
    columns="product_id",
    values="rating",
    fill_value=0
)

print("Calculating similarities...")

user_similarity = cosine_similarity(user_item_matrix)

print("Similarity Matrix Shape:", user_similarity.shape)
user_ids = user_item_matrix.index

target_user = user_ids[0]

target_index = 0

similar_users = list(
    enumerate(user_similarity[target_index])
)

similar_users = sorted(
    similar_users,
    key=lambda x: x[1],
    reverse=True
)

print(f"\nTarget User: {target_user}")

print("\nTop 5 Similar Users:")

target_user = user_ids[0]

target_products = set(
    df[df["user_id"] == target_user]["product_id"]
)

recommendations = {}

for idx, score in similar_users[1:6]:

    similar_user_id = user_ids[idx]

    similar_user_products = df[
        df["user_id"] == similar_user_id
    ]

    for _, row in similar_user_products.iterrows():

        product = row["product_id"]

        if product not in target_products:

            recommendations[product] = (
                recommendations.get(product, 0)
                + score
            )

top_products = sorted(
    recommendations.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

print("\nRecommended Products:")

for product, score in top_products:
    print(product, round(score, 4))