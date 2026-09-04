from app.services.final_ranking_engine import (
    get_final_rankings,
    save_recommendations
)

from app.services.popularity_recommender import (
    get_popular_products
)


def get_hybrid_recommendations(user_id):

    ranked_products = get_final_rankings(user_id)

    # SAVE TO DATABASE
    save_recommendations(
        user_id,
        ranked_products
    )

    popular = get_popular_products()

    return {
        "user_id": user_id,
        "ranked_recommendations": ranked_products[:10],
        "popular_products": popular[:5]
    }