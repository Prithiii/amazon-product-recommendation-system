similarity_df = pd.DataFrame(
    user_similarity,
    index=user_item_matrix.index,
    columns=user_item_matrix.index
)

similarity_df.to_parquet(
    "data/models/user_similarity.parquet"
)

print("Similarity matrix saved.")