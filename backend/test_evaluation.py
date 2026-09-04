from app.services.collaborative_recommender import get_recommendations

user_id = "AE224GVO7OHTYF26U6ER6BEVIUAQ"

recs = get_recommendations(user_id)

print(f"Total recommendations: {len(recs['recommended_products'])}")
print(recs['recommended_products'][:5])