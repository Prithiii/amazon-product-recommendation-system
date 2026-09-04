import streamlit as st
import requests

st.title("📈 Recommendation Model Evaluation")

user_id = st.text_input(
    "Enter User ID"
)

if st.button("Evaluate"):

    response = requests.get(
        f"http://127.0.0.1:8000/evaluation/{user_id}"
    )

    data = response.json()

    st.metric(
        "Precision@10",
        data["precision_at_10"]
    )

    st.metric(
        "Recall@10",
        data["recall_at_10"]
    )

    st.metric(
        "Hit Rate",
        data["hit_rate"]
    )