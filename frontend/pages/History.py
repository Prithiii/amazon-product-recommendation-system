import streamlit as st
import pandas as pd
import requests

st.title("📜 Recommendation History")

user_id = st.text_input("User ID")

if st.button("Load History"):

    response = requests.get(
        f"http://127.0.0.1:8000/history/{user_id}"
    )

    data = response.json()

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)