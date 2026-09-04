from app.services.collaborative_recommender import get_recommendations

user_id = "AE23LDQTB7L76AP6E6WPBFVYL5DA"

result = get_recommendations(user_id)

print(result)