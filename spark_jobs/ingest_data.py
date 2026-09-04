from datasets import load_dataset
import pandas as pd
import os

print("Loading dataset...")

dataset = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023",
    "0core_rating_only_Electronics",
    trust_remote_code=True
)

sample = dataset["full"].select(range(500000))

df = sample.to_pandas()

print("Cleaning data...")

df["rating"] = df["rating"].astype(float)

df["timestamp"] = pd.to_datetime(
    df["timestamp"].astype("int64"),
    unit="ms"
)

os.makedirs("data/processed", exist_ok=True)

df.to_parquet(
    "data/processed/electronics_sample.parquet",
    index=False
)

print("Data saved successfully.")