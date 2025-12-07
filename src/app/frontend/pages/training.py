import polars as pl
import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000/train/train"


def training_page() -> None:
    st.write("# Model Training Page")
    st.write("Upload a PGN file to train the chess game prediction model.")

    uploaded_file = st.file_uploader(
        "Choose a PGN file",
        type=["pgn"],
        help="Upload a chess games file in PGN format",
    )

    if st.button("Train Model", type="primary", disabled=uploaded_file is None):
        if uploaded_file is None:
            st.warning("Please upload a file first.")
            return

        with st.spinner("Training model... This may take a few minutes."):
            try:
                # Prepare the file for upload
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        "application/octet-stream",
                    )
                }

                response = requests.post(API_BASE_URL, files=files, timeout=3000)
                result = response.json()

                df = pl.DataFrame({
                    "Response Key": list(result.keys()),
                    "Value": [str(v) for v in result.values()],
                })

                if response.ok:
                    st.success("✅ Model trained successfully!")

                else:
                    st.error(f"❌ Training failed: {response.status_code}")
                st.dataframe(df)  # pyright: ignore[reportUnknownMemberType]

            except requests.exceptions.Timeout:
                st.error(
                    "❌ Request timed out. The training process is taking too long."
                )
            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Could not connect to the API. Make sure the backend is running."
                )
