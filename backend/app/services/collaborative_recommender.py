import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix


def get_recommendations(target_user):

    print("Connecting to PostgreSQL...")

    engine = create_engine(
        "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
    )

    print("Loading data...")

    query = """
    SELECT user_id, product_id, rating
    FROM interactions
    LIMIT 100000;
    """

    df = pd.read_sql(query, engine)

    print(f"Original Shape: {df.shape}")

    test_user = "AE23LDQTB7L76AP6E6WPBFVYL5DA"

    print(
    "Interactions for target user:",
    len(df[df["user_id"] == test_user])
)

    # Filter active users
    user_counts = df["user_id"].value_counts()
    active_users = user_counts[user_counts >= 5].index

    # Filter active products
    product_counts = df["product_id"].value_counts()
    active_products = product_counts[product_counts >= 3].index

    df = df[
        (df["user_id"].isin(active_users))
        &
        (df["product_id"].isin(active_products))
    ]

    print(f"Filtered Shape: {df.shape}")
    print(f"Unique Users: {df['user_id'].nunique()}")
    print(f"Unique Products: {df['product_id'].nunique()}")

    # Build User-Item Matrix
    print("\nBuilding User-Item Matrix...")

    user_item_matrix = df.pivot_table(
        index="user_id",
        columns="product_id",
        values="rating",
        fill_value=0
    )

    print(f"Matrix Shape: {user_item_matrix.shape}")

    # Check if target user exists
    user_ids = user_item_matrix.index.tolist()

    if target_user not in user_ids:
        target_user = user_ids[0]
        print("Using fallback user:", target_user)
        

    print("\nConverting to Sparse Matrix...")

    sparse_matrix = csr_matrix(
        user_item_matrix.values
    )

    print("Calculating User Similarities...")

    user_similarity = cosine_similarity(
        sparse_matrix,
        dense_output=False
    )

    print("Similarity Calculation Complete")

    target_index = user_ids.index(target_user)

    similarity_scores = list(
        zip(
            range(len(user_ids)),
            user_similarity[target_index].toarray()[0]
        )
    )

    similar_users = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    target_products = set(
        df[df["user_id"] == target_user]["product_id"]
    )

    recommendations = {}

    print("\nGenerating Recommendations...")

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

    return {
        "target_user": target_user,
        "recommended_products": [
            {
                "product_id": product,
                "score": round(score, 4)
            }
            for product, score in top_products
        ]
    }


# Run directly for testing
if __name__ == "__main__":

    engine = create_engine(
        "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
    )

    df = pd.read_sql("""
        SELECT user_id, product_id, rating
        FROM interactions
        LIMIT 100000;
    """, engine)

    user_counts = df["user_id"].value_counts()
    active_users = user_counts[user_counts >= 5].index

    df = df[df["user_id"].isin(active_users)]

    valid_user = df["user_id"].iloc[0]

    print("Testing User:", valid_user)

    result = get_recommendations(valid_user)

    print("\nRESULT:")
    print(result)