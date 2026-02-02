import requests
import streamlit as st

from app.frontend.settting import FrontendSettings


def health_page() -> None:
    st.write("# Health Page")

    if not st.button("Show Results"):
        return

    response = requests.get(FrontendSettings.HEALTH_API_URL, timeout=5)

    if not response.ok:
        st.error(f"There was an error in the request: {response.text}")
        return

    st.success(f"Prediction: {response.json()}")
