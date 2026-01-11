import requests
import streamlit as st

from app.frontend.settting import FrontendSettings

HEALTH_URL = FrontendSettings().HEALTH_API_URL


def health_page() -> None:
    st.write("# Health Page")

    if not st.button("Show Results"):
        return

    response = requests.get(HEALTH_URL, timeout=5)
    if response.ok:
        st.success(f"Prediction: {response.json()}")
        return

    st.error(f"There was an error in the request: {response.text}")
