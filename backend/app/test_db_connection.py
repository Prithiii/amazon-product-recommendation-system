from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
)

with engine.connect() as conn:
    print("Connected Successfully!")