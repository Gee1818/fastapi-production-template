import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000/train/train"


def training_page() -> None:
    st.write("# Model Training Page")
    st.write("Upload a PGN file to train the chess game prediction model.")

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a PGN file",
        type=["pgn"],
        help="Upload a chess games file in PGN format",
    )

    # Train button
    if st.button("Train Model", type="primary", disabled=uploaded_file is None):
        if uploaded_file is None:
            st.warning("Please upload a file first.")
            return

        # Show loading spinner
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

                # Make POST request to training endpoint
                response = requests.post(API_BASE_URL, files=files, timeout=3000)

                # Handle response
                if response.ok:
                    result = response.json()
                    st.success("✅ Model trained successfully!")
                    st.json(result)
                else:
                    st.error(f"❌ Training failed: {response.status_code}")

                    error_detail = response.json()
                    st.error(f"Error details: {error_detail}")

            except requests.exceptions.Timeout:
                st.error(
                    "❌ Request timed out. The training process is taking too long."
                )
            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Could not connect to the API. Make sure the backend is running."
                )
