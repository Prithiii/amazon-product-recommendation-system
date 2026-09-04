from app.services.recommendation_engine import (
    get_hybrid_recommendations
)

user_id = ""

results = get_hybrid_recommendations(
    user_id
)

print(results)