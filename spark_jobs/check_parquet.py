import pandas as pd

df = pd.read_parquet(
    "../data/processed/electronics_sample.parquet"
)

print(df.columns.tolist())
print(df.head())