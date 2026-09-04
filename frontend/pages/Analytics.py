import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

st.title("Recommendation Analytics")

engine = create_engine(
    "postgresql://postgres:Admin@localhost:5432/amazon_recommender"
)

# Load recommendation history
query = """
SELECT *
FROM recommendation_logs
ORDER BY created_at DESC
"""

df = pd.read_sql(query, engine)
st.subheader("System Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Recommendations",
    len(df)
)

col2.metric(
    "Unique Users",
    df["user_id"].nunique()
)

col3.metric(
    "Unique Products",
    df["recommended_product"].nunique()
)

col4.metric(
    "Average Score",
    round(df["score"].mean(), 2)
)
st.subheader("Top Active Users")

top_users = (
    df.groupby("user_id")
      .size()
      .reset_index(name="recommendations_generated")
      .sort_values(
          "recommendations_generated",
          ascending=False
      )
)

st.dataframe(
    top_users,
    use_container_width=True
)
st.subheader("Most Recommended Products")

top_products = (
    df.groupby("recommended_product")
      .size()
      .reset_index(name="recommendation_count")
      .sort_values(
          "recommendation_count",
          ascending=False
      )
)

st.dataframe(
    top_products,
    use_container_width=True
)
st.subheader("Recommendation Score Distribution")

fig = px.histogram(
    df,
    x="score",
    nbins=20,
    title="Distribution of Recommendation Scores"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
if df.empty:
    st.warning("No recommendation data found")
    st.stop()

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Recommendations",
    len(df)
)

col2.metric(
    "Unique Users",
    df["user_id"].nunique()
)

col3.metric(
    "Unique Products",
    df["recommended_product"].nunique()
)

st.divider()

# Top Products
st.subheader("Top Recommended Products")

top_products = (
    df.groupby("recommended_product")
      .size()
      .reset_index(name="count")
      .sort_values("count", ascending=False)
      .head(10)
)

st.dataframe(top_products)

# Trend Chart
st.subheader("Recommendation Trend")

trend_df = (
    df.groupby(
        pd.to_datetime(df["created_at"]).dt.date
    )
    .size()
    .reset_index(name="recommendations")
)

fig = px.line(
    trend_df,
    x="created_at",
    y="recommendations",
    title="Recommendations Generated Over Time"
)

st.plotly_chart(
    fig,
    use_container_width=True
)