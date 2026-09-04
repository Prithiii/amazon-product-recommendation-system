from app.services.final_ranking_engine import get_final_rankings

user_id = "AE23LDQTB7L76AP6E6WPBFVYL5DA"  # use a valid user from your dataset

result = get_final_rankings(user_id)

print(result)