import streamlit as st
import requests
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="Amazon Recommendation Dashboard",
    layout="wide"
)

st.title("Amazon-Style Personalized Product Recommendation System")

user_id = st.text_input("Enter User ID")

if st.button("Get Recommendations"):

    if user_id:

        try:

            # FastAPI endpoint
            response = requests.get(
                f"http://127.0.0.1:8000/ranked/{user_id}"
            )

            if response.status_code != 200:
                st.error(f"API Error: {response.text}")
                st.stop()

            data = response.json()

            st.success("Recommendations Loaded")

            st.subheader("🎯 Recommended Products")

            for i, item in enumerate(
                data["ranked_recommendations"], start=1
            ):

                st.markdown(
                    f"""
            ### {i}. {item['product_name']}

            **Product ID:** {item['product_id']}

            **Category:** {item['category']}

            ⭐ **Average Rating:** {item['avg_rating']}

            🏆 **Priority Score:** {item['priority_score']}

            ---
"""
    )


            st.subheader("🎯 Recommended Products")

            for i, item in enumerate(
                data["ranked_recommendations"], start=1
            ):

                st.markdown(
                    f"""
            ### {i}. {item['product_name']}

            **Product ID:** {item['product_id']}

            **Category:** {item['category']}

            ⭐ **Average Rating:** {item['avg_rating']}

            🏆 **Priority Score:** {item['priority_score']}

            ---
            """
                )
            st.subheader("🔥 Popular Products")

            for item in data["popular_products"]:

                st.markdown(
                    f"""
            **Product ID:** {item['product_id']}

            ⭐ Rating: {item['avg_rating']}

            📝 Reviews: {item['total_reviews']}

            ---
            """
                )

            st.subheader("Recommendation History")

            history_response = requests.get(
                f"http://127.0.0.1:8000/history/{user_id}"
            )

            if history_response.status_code == 200:

                history_data = history_response.json()

                if len(history_data) > 0:

                    history_df = pd.DataFrame(history_data)

                    st.dataframe(
                        history_df,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No recommendation history found"
                    )

            else:

                st.warning(
                    "History endpoint not available"
                )

        except Exception as e:

            st.error(str(e))
        